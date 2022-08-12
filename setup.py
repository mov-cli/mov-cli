from setuptools import setup, find_packages
from mov_cli.version.__version__ import __core__


with open("requirements.txt") as requirements_txt:
    requirements = requirements_txt.read().splitlines()

setup(
    name="mov-cli",
    version=__core__,
    author="pain@poseidon444",
    author_email="painedposeidon444@gmail.com",
    description="A module to download and stream your favorite movies and series.",
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
)
