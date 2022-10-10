from setuptools import setup, find_packages


with open("requirements.txt") as requirements_txt:
    requirements = requirements_txt.read().splitlines()

with open("readme.md") as readme_md:
    readme = readme_md.read()

setup(
    name="mov-cli",
    version="0.1.8",
    author="pain@poseidon444",
    author_email="painedposeidon444@gmail.com",
    maintainer="ananas@r3tr0ananas",
    maintainer_email="r3tr0ananas@hotmail.com",
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
    long_description=f"{readme}",
)
