from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Literal

    from ..media import Media
    from ..players import Player
    from ..utils.platform import SUPPORTED_PLATFORMS

import time
from subprocess import Popen

from .ui import prompt
from ..media import Series

__all__ = (
    "watch_options", 
)

def watch_options(
    popen: Popen, 
    player: Player, 
    platform: SUPPORTED_PLATFORMS, 
    media: Media, 
    fzf_enabled: bool
) -> Optional[Literal["search", "next", "previous", "select"]]:
    options = [
        "search",
        "replay",
        "quit"
    ]

    if isinstance(media, Series):
        options.insert(0, "next")
        options.insert(1, "previous")
        options.insert(2, "select")

    if platform == "iOS":
        time.sleep(3) # so iOS mfs have time to read the "pasted to clipboard" prompt. (untested 👍) lmao

    choice = prompt(
        text = f"Playing '{media.display_name}'", 
        choices = options, 
        display = lambda x: x, 
        fzf_enabled = fzf_enabled
    )

    if choice == "quit":
        popen.kill()

    elif choice == "replay":
        popen.kill()

        new_popen = player.play(media)

        return watch_options(
            new_popen, player, platform, media, fzf_enabled
        )

    return choice