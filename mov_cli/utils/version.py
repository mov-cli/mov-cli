from __future__ import annotations

import httpx
import mov_cli

__all__ = ("update_available",)

def update_available() -> bool:
    pypi = httpx.get("https://pypi.org/pypi/mov-cli/json").json()
    pypi_ver = pypi["info"]["version"]

    if pypi_ver > mov_cli.__version__:
        return True

    return False