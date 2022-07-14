from setuptools import setup, find_packages

setup(
    name="mov-cli",
    version="0.1.0",
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
    install_requires=["click", "httpx", "bs4", "colorama"],
    entry_points="""
        [console_scripts]
        mov-cli=mov_cli:main.main
    """,
)
