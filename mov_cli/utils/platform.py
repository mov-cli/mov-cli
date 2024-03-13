from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal

    SUPPORTED_PLATFORMS = Literal["Windows", "Linux", "Android", "Darwin", "iOS"]

import sys
import platform

__all__ = ("what_platform",)

def what_platform() -> SUPPORTED_PLATFORMS:
    """
    Returns what platform/OS this device is running on.

    E.g. Windows, Linux, Android, Darwin, iOS
    """
    os = platform.system()

    if os == "Linux":
        if hasattr(sys, "getandroidapilevel"):
            return "Android"
        elif "-ish" in platform.platform():
            return "iOS"

        return os

    return os
