<a name="readme-top"></a>

[![Stargazers][stars-shield]][stars-url]
[![Pypi Version][pypi-shield]][pypi-url]
[![Python Versions][python-shield]][pypi-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Discord][discord-shield]][discord-url]

<div align="center">

  <a href="https://github.com/mov-cli/mov-cli">
    <img src="https://github.com/mov-cli/mov-cli/assets/132799819/a23bec13-881d-41b9-b596-b31c6698b89e" alt="Logo" width="250">
  </a>

  <sub>Watch everything from your terminal.</sub>
  <br>
  <br>
  <a href="https://github.com/mov-cli/mov-cli/issues">Report Bug</a>
  ·
  <a href="https://github.com/mov-cli/mov-cli/issues">Request Feature</a>

</div>

<br>

> [!Note]
> v4 is constantly changing so be sure to keep the tool up to date and with that said I would advise not using it as a library yet.

## Installation 🛠️

> [!TIP]
> For in-depth installation instructions hit the [wiki](https://github.com/mov-cli/mov-cli/wiki/Installation).

### Prerequisites
- **A supported platform:**
  - Linux
  - Windows
  - Android (via [Termux](https://termux.dev/en/))
  - iOS (via [iSH Shell](https://ish.app/))
  - *MacOS* (**Not tested**)
- **[python](https://www.python.org/downloads/)** (**required**, with pip)
- **[lxml](https://pypi.org/project/lxml/)** (optional, ⚡ faster scraping)
- **[fzf](https://github.com/junegunn/fzf?tab=readme-ov-file#installation)** (optional but **highly recommended**)
- **[mpv](https://mpv.io/installation/)** (recommended & default media player)

To get running these are all the prerequisites you'll need.

With the prerequisites installed, mov-cli can be installed via the pip command on all platforms with Python version 3.8 or above.

```sh
pip install mov-cli -U
```

## Usage 🖱️
mov-cli comes packaged with a CLI interface via the `mov-cli` command you can use in your respective terminal. 

> [!NOTE]
> You may notice mov-cli doesn't ship with any scrapers (or previously known as providers) by default, this is because v4 is plugin-based and scrapers are now part of plugins that must be chosen to be installed.
> Find out how to do so at the [wiki](https://github.com/mov-cli/mov-cli/wiki#plugins).

1. Install the scraper plugin of your choice. Visit this [wiki page](https://github.com/mov-cli/mov-cli/wiki/Plugins) on how to do so and the [mov-cli-plugin](https://github.com/topics/mov-cli-plugin) topic for a list of **third-party** mov-cli plugins.
```sh
mov-cli -e
```
```toml
[mov-cli.plugins]
films = "package_name"
```

2. Scraper away!
```sh
mov-cli -s films spider man no way home
```
<img width="370px" src="https://github.com/mov-cli/mov-cli/assets/66202304/86189cab-b246-405e-a266-6c624bee2d36">

> The above command should search for `spider man no way home` with the following scraper.

## Contributing ✨
Pull requests are welcome and *appreciated*. For major changes, please open an issue first to discuss what you would like to change.

<a href = "https://github.com/mov-cli/mov-cli/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=mov-cli/mov-cli"/>
</a>

## Inspiration 🌟
Inspired by [ani-cli](https://github.com/pystardust/ani-cli), [lobster](https://github.com/justchokingaround/lobster) and [animdl](https://github.com/justfoolingaround/animdl)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/mov-cli/mov-cli.svg?style=for-the-badge
[contributors-url]: https://github.com/mov-cli/mov-cli/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mov-cli/mov-cli.svg?style=for-the-badge
[forks-url]: https://github.com/mov-cli/mov-cli/network/members
[stars-shield]: https://img.shields.io/github/stars/mov-cli/mov-cli?style=flat
[stars-url]: https://github.com/mov-cli/mov-cli/stargazers
[pypi-shield]: https://img.shields.io/pypi/v/mov-cli?style=flat
[pypi-url]: https://pypi.org/project/mov-cli/
[python-shield]: https://img.shields.io/pypi/pyversions/mov-cli?style=flat
[issues-shield]: https://img.shields.io/github/issues/mov-cli/mov-cli?style=flat
[issues-url]: https://github.com/mov-cli/mov-cli/issues
[license-shield]: https://img.shields.io/github/license/mov-cli/mov-cli?style=flat
[license-url]: ./LICENSE
[discord-shield]: https://img.shields.io/badge/Discord-7289da?logo=discord&logoColor=white
[discord-url]: https://discord.gg/BMzC7ePsBV
