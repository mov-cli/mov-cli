from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal

    SUPPORTED_PLATFORMS = Literal["Windows", "Linux", "Android", "Darwin", "iOS", "FreeBSD"]

import sys
import platform
import csv

__all__ = ("what_platform",)

def what_platform() -> SUPPORTED_PLATFORMS:
    """
    Returns what platform/OS this device is running on.

    E.g. Windows, Linux, Android, Darwin, iOS, FreeBSD
    """
    os = platform.system()

    if os == "Linux":
        if hasattr(sys, "getandroidapilevel"):
            return "Android"
        elif "-ish" in platform.platform():
            return "iOS"

        return os

    return os

def what_distro() -> str | None:
    """
    Returns what linux distro this device is running on.

    E.g. arch, ubuntu, debian
    """
    RELEASE_DATA = {}

    if what_platform() == "Linux":
        with open("/etc/os-release", "r") as f:
            os_release = csv.reader(f, delimiter="=")
            for row in os_release:
                if row:
                    RELEASE_DATA[row[0]] = row[1]

        return RELEASE_DATA["ID"]    

    return None