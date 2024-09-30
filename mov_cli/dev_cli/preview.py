from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

    from pathlib import Path

import re
import os
import httpx
import typer
import shutil
import subprocess
import unicodedata

from ..cache import Cache
from ..utils import what_platform, get_temp_directory

__all__ = ()

preview_app = typer.Typer(
    name = "preview", 
    help = "Dev command used by stuff like fzf to display images from mov-cli in the terminal."
)

@preview_app.command(help = "Preview image and information of mov-cli cached metadata to terminal.")
def metadata(id: str):
    platform = what_platform()

    if not platform == "Linux" and not platform == "FreeBSD" and not platform == "Android":
        print("Image preview only works on Linux, Android an FreeBSD atm.")
        return False

    cache = Cache(
        platform = platform, 
        section = "metadata_preview"
    )

    preview_data = cache.get_cache(id) # TODO: Type dict preview data.

    details: Optional[str] = preview_data.get("details")
    image_url: Optional[str] = preview_data.get("image_url")

    if image_url is None and details is None:
        print("No image & details available\nto preview for this metadata.")
        raise typer.Exit(0)

    if image_url is not None:
        fzf_preview_lines = os.environ["FZF_PREVIEW_LINES"] # height
        fzf_preview_columns = os.environ["FZF_PREVIEW_COLUMNS"] # width

        os.system("clear")

        if "KITTY_WINDOW_ID" in os.environ:
            subprocess.call([
                "kitty", 
                "icat", 
                "--clear", 
                "--transfer-mode=memory", 
                "--unicode-placeholder", 
                "--stdin=no", 
                f"--place={fzf_preview_columns}x{fzf_preview_lines}@0x0", 
                "--scale-up", 
                image_url
            ])

        elif shutil.which("chafa") is not None:
            file = image_url_to_file(image_url, id, platform).resolve()

            subprocess.call([
                "chafa", 
                file, 
                f"--size={fzf_preview_columns}x{fzf_preview_lines}", 
                "--clear"
            ])

        else:
            print("'chafa' was not found hence image cannot be displayed! :( Please install it: https://github.com/hpjansson/chafa")

    if details is not None:
        print("\n" + details)

def image_url_to_file(image_url: str, id: str, platform: str) -> Optional[Path]:
    temp = get_temp_directory(platform)
    file = temp.joinpath(slugify(id))

    if file.exists():
        return file

    request = httpx.get(image_url)

    if request.is_error:
        return None

    with file.open("wb") as f:
        f.write(request.content)

    return file

def slugify(value): # https://github.com/django/django/blob/main/django/utils/text.py#L452-L469
    value = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
    )

    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")