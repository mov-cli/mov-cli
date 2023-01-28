# -*- coding: utf-8 -*-
"""
    ResolveUrl Kodi Addon
    Copyright (C) 2013 Bstrdsmkr
    Additional fixes by mortael, jairoxyz
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    Adapted for use in xbmc from:
    https://github.com/beautify-web/js-beautify/blob/master/python/jsbeautifier/unpackers/packer.py
    Unpacker for Dean Edward's p.a.c.k.e.r, a part of javascript beautifier
    by Einar Lielmanis <einar@jsbeautifier.org>
        written by Stefano Sanfilippo <a.little.coder@gmail.com>
    usage:
    if detect(some_string):
        unpacked = unpack(some_string)
    Unpacker for Dean Edward's p.a.c.k.e.r
"""

import re
import binascii
from six import PY2


def detect(source):
    """Detects whether `source` is P.A.C.K.E.R. coded."""
    mystr = re.search(
        r"eval[ ]*\([ ]*function[ ]*\([ ]*p[ ]*,[ ]*a[ ]*,[ ]*c["
        r" ]*,[ ]*k[ ]*,[ ]*e[ ]*,[ ]*",
        source,
    )
    return mystr is not None


def unpack(source):
    """Unpacks P.A.C.K.E.R. packed js code."""
    payload, symtab, radix, count = _filterargs(source)

    if count != len(symtab):
        raise UnpackingError('Malformed p.a.c.k.e.r. symtab.')

    try:
        unbase = Unbaser(radix)
    except TypeError:
        raise UnpackingError('Unknown p.a.c.k.e.r. encoding.')

    def lookup(match):
        """Look up symbols in the synthetic symtab."""
        word = match.group(0)
        return symtab[int(word)] if radix == 1 else symtab[unbase(word)] or word

    def getstring(c, a=radix):
        foo = chr(c % a + 161)
        if c < a:
            return foo
        else:
            return getstring(int(c / a), a) + foo

    payload = payload.replace("\\\\", "\\").replace("\\'", "'")
    p = re.search(r'eval\(function\(p,a,c,k,e.+?String\.fromCharCode\(([^)]+)', source)
    if p:
        pnew = re.findall(r'String\.fromCharCode\(([^)]+)', source)[0].split('+')[1] == '161'
    else:
        pnew = False

    if pnew:
        for i in range(count - 1, -1, -1):
            payload = payload.replace(getstring(i).decode('latin-1') if PY2 else getstring(i), symtab[i])
        return _replacejsstrings((_replacestrings(payload)))
    else:
        source = re.sub(r"\b\w+\b", lookup, payload) if PY2 else re.sub(r"\b\w+\b", lookup, payload, flags=re.ASCII)
        return _replacestrings(source)


def _filterargs(source):
    """Juice from a source file the four args needed by decoder."""
    argsregex = r"}\s*\('(.*)',\s*(.*?),\s*(\d+),\s*'(.*?)'\.split\('\|'\)"
    args = re.search(argsregex, source, re.DOTALL).groups()

    try:
        payload, radix, count, symtab = args
        radix = 36 if not radix.isdigit() else int(radix)
        return payload, symtab.split('|'), radix, int(count)
    except ValueError:
        raise UnpackingError('Corrupted p.a.c.k.e.r. data.')


def _replacestrings(source):
    """Strip string lookup table (list) and replace values in source."""
    match = re.search(r'var *(_\w+)=\["(.*?)"];', source, re.DOTALL)

    if match:
        varname, strings = match.groups()
        startpoint = len(match.group(0))
        lookup = strings.split('","')
        variable = '%s[%%d]' % varname
        for index, value in enumerate(lookup):
            if '\\x' in value:
                value = value.replace('\\x', '')
                value = binascii.unhexlify(value).decode('ascii')
            source = source.replace(variable % index, '"%s"' % value)
        return source[startpoint:]
    return source


def _replacejsstrings(source):
    """Strip JS string encodings and replace values in source."""
    match = re.findall(r'\\x([0-7][0-9A-F])', source)

    if match:
        match = set(match)
        for value in match:
            source = source.replace('\\x{0}'.format(value), binascii.unhexlify(value).decode('ascii'))

    return source


class Unbaser(object):
    """Functor for a given base. Will efficiently convert
    strings to natural numbers."""
    ALPHABET = {
        62: '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        95: (r' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
             r'[\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
    }

    def __init__(self, base):
        self.base = base

        # If base can be handled by int() builtin, let it do it for us
        if 2 <= base <= 36:
            self.unbase = lambda string: int(string, base)
        else:
            if base < 62:
                self.ALPHABET[base] = self.ALPHABET[62][0:base]
            elif 62 < base < 95:
                self.ALPHABET[base] = self.ALPHABET[95][0:base]
            # Build conversion dictionary cache
            try:
                self.dictionary = dict(
                    (cipher, index) for index, cipher in enumerate(
                        self.ALPHABET[base]))
            except KeyError:
                raise TypeError('Unsupported base encoding.')

            self.unbase = self._dictunbaser

    def __call__(self, string):
        return self.unbase(string)

    def _dictunbaser(self, string):
        """Decodes a  value to an integer."""
        ret = 0
        for index, cipher in enumerate(string[::-1]):
            ret += (self.base ** index) * self.dictionary[cipher]
        return ret


class UnpackingError(Exception):
    """Badly packed source or general error. Argument is a
    meaningful description."""
    pass