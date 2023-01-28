"""
Module containing the base class of all players.
"""
from __future__ import annotations

import platform
import subprocess
from os import environ
import abc
import sys

# Base Class
#--------------
class Player():
    """A base class for players in mov-cli."""
    def __init__(self, display_name:str) -> None:
        __metaclass__ = abc.ABCMeta

        self.__display_name = display_name

        self.__os = platform.system()

    @property
    def display_name(self) -> str:
        """Returns display name of player."""
        return self.__display_name

    @property
    def os(self) -> str:
        """
        Returns the operating system we're currently running on. (Adds android detection.)
        
        E.g. Windows, Linux, Android, Darwin
        """
        if self.__os == "Linux":
            if hasattr(sys, 'getandroidapilevel'):
                return "Android"
            return self.__os
        else:
            return self.__os

    @abc.abstractmethod
    def play(self, url:str, referrer:str, media_title:str) -> subprocess.Popen:
        """Method to be overridden with code for playing media in that particular player."""
        pass

# Exceptions
#--------------
class PlayerNotFound(Exception):
    """Raise when player is not found."""
    def __init__(self, player:Player) -> None:
        super().__init__(f"'{player.display_name}' was not found. Are you sure you have it installed? Are you sure the environment variable is set properly.")
