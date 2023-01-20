from setuptools import setup, find_packages
from pathlib import Path

with open("requirements.txt") as requirements_txt:
    requirements = requirements_txt.read().splitlines()

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mov-cli",
    version="0.6.9",
    author="pain@poseidon444",
    author_email="painedposeidon444@gmail.com",
    maintainer="ananas@r3tr0ananas",
    maintainer_email="r3tr0ananas@hotmail.com",
    description="A module to download and stream your favorite movies and shows.",
    packages=find_packages(),
    url="https://github.com/mov-cli/mov-cli",
    keywords=[
        "stream",
        "series",
        "series-stream",
        "tv shows" "twist",
        "download",
        "free",
        "movies",
        "mov-cli",
        "movie-streamer",
        "theflix",
        "actvid",
        "sflix",
        "solar",
        "olgply",
    ],
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        mov-cli=mov_cli.__main__:movcli
    """,
    long_description_content_type="text/markdown",
    long_description=long_description,
)
