"""
Ported over from [goldy's fork](https://github.com/THEGOLDENPRO/iterfzf/) of [iterfzf](https://github.com/dahlia/iterfzf) 
as of [issue #238](https://github.com/mov-cli/mov-cli/issues/238).

Source code changes can be seen [here](https://github.com/THEGOLDENPRO/iterfzf/commits/main/).
"""

from __future__ import print_function, annotations
from typing import TYPE_CHECKING

import sys
import errno
import subprocess
from os import fspath, PathLike

if TYPE_CHECKING:
    from typing import AnyStr, Iterable, Literal, Optional, Tuple, TypeVar

    T = TypeVar("T")

__all__ = (
    '__fzf_version__', 
    '__version__', 
    'BUNDLED_EXECUTABLE', 
    'iterfzf'
)

__fzf_version__ = '0.42.0'
__version__ = '1.0.' + __fzf_version__

POSIX_EXECUTABLE_NAME: Literal['fzf'] = 'fzf'
WINDOWS_EXECUTABLE_NAME: Literal['fzf.exe'] = 'fzf.exe'
EXECUTABLE_NAME: Literal['fzf', 'fzf.exe'] = \
    WINDOWS_EXECUTABLE_NAME \
    if sys.platform == 'win32' \
    else POSIX_EXECUTABLE_NAME


def iterfzf(
    iterable: Iterable[Tuple[AnyStr, T]],
    *,
    # Search mode:
    extended: bool = True,
    exact: bool = False,
    case_sensitive: bool = None,
    # Interface:
    multi: bool = False,
    mouse: bool = True,
    print_query: bool = False,
    # Layout:
    prompt: str = '> ',
    ansi: bool = False,
    preview: Optional[str] = None,
    # Misc:
    query: str = '',
    encoding: Optional[str] = None,
    executable: PathLike = EXECUTABLE_NAME
):
    cmd = [fspath(executable), '--no-sort', '--prompt=' + prompt]
    if not extended:
        cmd.append('--no-extended')
    if case_sensitive is not None:
        cmd.append('+i' if case_sensitive else '-i')
    if exact:
        cmd.append('--exact')
    if multi:
        cmd.append('--multi')
    if not mouse:
        cmd.append('--no-mouse')
    if print_query:
        cmd.append('--print-query')
    if query:
        cmd.append('--query=' + query)
    if preview:
        cmd.append('--preview=' + preview)
    if ansi:
        cmd.append('--ansi')
    encoding = encoding or sys.getdefaultencoding()
    proc = None
    stdin = None
    byte = None
    lf = u'\n'
    cr = u'\r'
    for line in iterable:
        line = line[0]

        if byte is None:
            byte = isinstance(line, bytes)
            if byte:
                lf = b'\n'
                cr = b'\r'
        elif isinstance(line, bytes) is not byte:
            raise ValueError(
                'element values must be all byte strings or all '
                'unicode strings, not mixed of them: ' + repr(line)
            )
        if lf in line or cr in line:
            raise ValueError(
                r"element values must not contain CR({1!r})/"
                r"LF({2!r}): {0!r}".format(line, cr, lf)
            )
        if proc is None:
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=None
            )
            stdin = proc.stdin
        if not byte:
            line = line.encode(encoding)
        try:
            stdin.write(line + b'\n')
            stdin.flush()
        except IOError as e:
            if e.errno != errno.EPIPE and errno.EPIPE != 32:
                raise
            break
    if proc is None or proc.wait() not in [0, 1]:
        if print_query:
            return None, None
        else:
            return None
    try:
        stdin.close()
    except IOError as e:
        if e.errno != errno.EPIPE and errno.EPIPE != 32:
            raise
    stdout = proc.stdout
    decode = (lambda b: b) if byte else (lambda t: t.decode(encoding))
    output = [decode(ln.strip(b'\r\n\0')) for ln in iter(stdout.readline, b'')]
    if print_query:
        try:
            if multi:
                return output[0], output[1:]
            else:
                return output[0], output[1]
        except IndexError:
            return output[0], None
    else:
        if multi:
            return output
        else:
            try:
                return output[0]
            except IndexError:
                return None