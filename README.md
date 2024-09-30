<a name="readme-top"></a>

[![Stargazers][stars-shield]][stars-url]
[![Pypi Version][pypi-shield]][pypi-url]
[![Pypi Downloads][pypi-dl-shield]][pypi-stats-url]
[![Python Versions][python-shield]][pypi-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


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

  <br>
  <br>
  <a href="https://discord.gg/BMzC7ePsBV">
    <img src="https://invidget.switchblade.xyz/BMzC7ePsBV" alt="Logo" width="400">
  </a>

</div>
<br>

> [!Note]
> v4 is constantly changing so be sure to **keep the tool and your plugins up to date**. Also, I would advise not using it as a library yet as the API still has many breaking changes.

## What is mov-cli? 💫

<div align="center">

  <img width="800px" src="https://github.com/mov-cli/mov-cli/assets/66202304/fa78b38c-0df0-464a-a78e-cb8a04cdc885">

</div>

**mov-cli** is a command line tool with plugin support that streamlines the process of streaming media from the comfort of your terminal; ~~*so you can show off to your friends the superiority of the command line.*~~ 💪 The tool is sort of a framework that handles metadata, configuration and scraping of the media to be streamed in your media player of choice.

**mov-cli** [is **not** a piracy tool](./disclaimer.md); in fact, we encourage the opposite through the existence of our plugins [mov-cli-files](https://github.com/mov-cli/mov-cli-files) and [mov-cli-jellyplex](https://github.com/mov-cli/mov-cli-jellyplex). 🫵 You obtain the media. You pick the plugins.

## Installation 🛠️

> [!TIP]
> For in-depth installation instructions hit the [wiki](https://github.com/mov-cli/mov-cli/wiki/Installation).

### Prerequisites
- **A supported platform:**
  - Linux
  - Windows
  - FreeBSD (https://github.com/mov-cli/mov-cli/issues/359)
  - Android (via [Termux](https://termux.dev/en/))
  - iOS (via [iSH Shell](https://ish.app/))
  - MacOS
- **[python](https://www.python.org/downloads/)** (**required**, with pip)
- **[lxml](https://pypi.org/project/lxml/)** (optional, ⚡ faster scraping)
- **[fzf](https://github.com/junegunn/fzf?tab=readme-ov-file#installation)** (optional but **highly recommended**)
- **[mpv](https://mpv.io/installation/)** (recommended & default media player)

To get running these are all the prerequisites you'll need.

With the prerequisites installed, mov-cli can be installed via the pip command on all platforms with Python version ~~3.8~~ **3.9** or above **(3.8 is deprecated as of 4.5)**.

```sh
pip install mov-cli -U
```
> Check out the [wiki on installation](https://github.com/mov-cli/mov-cli/wiki/Installation) for more in-depth guidance on installing mov-cli.

## Usage 🖱️
[!showcase video](https://github.com/mov-cli/mov-cli/assets/132799819/d924c3f5-775c-46a3-97f5-ff27433b69dd)

mov-cli comes packaged with a CLI interface via the `mov-cli` command you can use in your respective terminal. 

> [!NOTE]
> You may notice mov-cli doesn't ship with any scrapers (or previously known as providers) by default, this is because v4 is plugin-based and scrapers are now part of plugins that must be chosen to be installed.
> Find out how to do so at the [wiki](https://github.com/mov-cli/mov-cli/wiki#plugins).

1. Install the plugin of your choice. Visit this [wiki page](https://github.com/mov-cli/mov-cli/wiki/Plugins) on how to do so and the [mov-cli-plugin](https://github.com/topics/mov-cli-plugin) topic for a list of **third-party** mov-cli plugins.
```sh
pip install mov-cli-youtube
```
> This is just an example.
> If you are struggling, visit that [wiki page](https://github.com/mov-cli/mov-cli/wiki/Plugins).

2. Add the plugin to your config.
```sh
mov-cli -e
```
Alternatively, you may also edit by manually opening the config file. See this [Wiki page](https://github.com/mov-cli/mov-cli/wiki/Configuration#introduction) on that.  
```toml
[mov-cli.plugins]
youtube = "mov-cli-youtube"
```
> Check out the [wiki](https://github.com/mov-cli/mov-cli/wiki/Plugins) for more in-depth explanation.

3. Scrape away!
```sh
mov-cli -s youtube blender studio
```
<img src="https://github.com/mov-cli/mov-cli/assets/132799819/f7a75a14-105b-4afa-9075-bb2d937baa25">

> The command above searches for `blender studio` with our [youtube](https://github.com/mov-cli/mov-cli-youtube) plugin, **however once again mov-cli is plugin based and there are many of them [in the wild](https://github.com/topics/mov-cli-plugin). 😉**

## Star Graph ⭐
[![Star Graph Chart](https://api.star-history.com/svg?repos=mov-cli/mov-cli&type=Date)](https://star-history.com/#mov-cli/mov-cli&Date)

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
[pypi-stats-url]: https://pypistats.org/packages/mov-cli
[python-shield]: https://img.shields.io/pypi/pyversions/mov-cli?style=flat
[issues-shield]: https://img.shields.io/github/issues/mov-cli/mov-cli?style=flat
[issues-url]: https://github.com/mov-cli/mov-cli/issues
[license-shield]: https://img.shields.io/github/license/mov-cli/mov-cli?style=flat
[license-url]: ./LICENSE
[pypi-dl-shield]: https://img.shields.io/pypi/dm/mov-cli?color=informational&label=pypi%20downloads
