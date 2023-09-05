<a name="readme-top"></a>

<div align="center">

  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]

  <a href="https://github.com/mov-cli/mov-cli">
    <img src="https://github.com/mov-cli/mov-cli/assets/132799819/a23bec13-881d-41b9-b596-b31c6698b89e" alt="Logo" width="200">
  </a>

  <sub>A cli tool to stream Movies, Shows, LIVE-TV and Sports.</sub>
  <br>
  <br>
  <a href="https://github.com/mov-cli/mov-cli/issues">Report Bug</a>
  ·
  <a href="https://github.com/mov-cli/mov-cli/issues">Request Feature</a>

</div>

### Table of Contents
<ol>
  <li>
    <a href="#about-the-project">About The Project</a>
  </li>
  <li>
    <a href="#getting-started">Getting Started</a>
    <ul>
      <li><a href="#prerequisites">Prerequisites</a></li>
      <li><a href="#installation">Installation</a></li>
      <ul>
        <li><a href="#windows--linux">Windows / Linux</a></li>
        <li><a href="#linux">Linux Builds</a></li>
        <li><a href="#android">Android</a></li>
        <li><a href="#ios">iOS</a></li>
      </ul>
    </ul>
  </li>
  <li><a href="#usage">Usage</a></li>
  <li><a href="#disclaimer">Disclaimer</a></li>
  <li><a href="#contributing">Contributing</a></li>
  <li><a href="#contact">Contact</a></li>
  <li><a href="#inspiration">inspiration</a></li>
</ol>

## About The Project

The new and improved mov-cli is here.

mov-cli is a Commandline Tool to watch and download shows and movies.

Shows and Movies are sourced from Streaming Sites.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started
### Prerequisites

- [`mpv`](https://mpv.io) - player used for Windows, Linux and Android
- [`iina`](https://iina.io) - player used for MacOS
- [`Outplayer`](https://outplayer.app/) - player used for iOS
- [`ffmpeg`](https://github.com/FFmpeg/FFmpeg) - For downloads 
- [`fzf`](https://github.com/junegunn/fzf) - The selection Menu


## Installation
### Windows / Linux
  - Run this Command inside your Terminal
    ``` 
    pip install mov-cli
    ```
  - Optional 
    ```
    pip install lxml
    ```

### Linux
There are MPR and AUR Builds.

- [MPR Build](https://mpr.makedeb.org/packages/mov-cli)
- [AUR Build](https://aur.archlinux.org/packages/mov-cli-git)

#### Disclaimer: They are not maintained by us.

### Android               
  - Make sure [MPV](https://play.google.com/store/apps/details?id=is.xyz.mpv) and [Termux](https://play.google.com/store/apps/details?id=com.termux) are installed.
  
  - Install ``mov-cli``.
    ```
    pip install mov-cli
    ```
  
  - Optional
    ```
    apt-get install libxml2 libxslt
    pip install lxml
    ```

### iOS
  - Make sure [Outplayer](https://apps.apple.com/us/app/outplayer/id1449923287) and [iSH](https://apps.apple.com/us/app/ish-shell/id1436902243) are installed.

  - Run following commands (Note: this may take a while)
    ```
    apk update && apk upgrade
    apk add python3 fzf
    python3 -m ensurepip
    pip3 install mov-cli
    ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
Type: ``mov-cli`` into your command line.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Disclaimer
This project is to be used at the user’s own risk, based on their government and laws.

This project has no control on the content it is serving, using copyrighted content from the providers is not going to be accounted for by the developer. It is the user’s own risk.

[[More on That]](./disclaimer.md)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Feature
If you want a feature, create an [issue](https://github.com/mov-cli/mov-cli/issues/new) or create the feature and make a pull request.
<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contributing
Pull requests are welcome and _appreciated_. For major changes, please open an issue first to discuss what you would like to change.

<a href = "https://github.com/mov-cli/mov-cli/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=mov-cli/mov-cli"/>
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact
- Author: **Poseidon444** | Discord: ``pain444``
- Maintainer: **R3tr0Ananas** | Discord: ``r3tr0ananas``
- Maintainer: **Goldy** | Discord: ``g0ldy_``

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Inspiration
Heavily inspired from [ani-cli](https://github.com/pystardust/ani-cli)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/mov-cli/mov-cli.svg?style=for-the-badge
[contributors-url]: https://github.com/mov-cli/mov-cli/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mov-cli/mov-cli.svg?style=for-the-badge
[forks-url]: https://github.com/mov-cli/mov-cli/network/members
[stars-shield]: https://img.shields.io/github/stars/mov-cli/mov-cli.svg?style=for-the-badge
[stars-url]: https://github.com/mov-cli/mov-cli/stargazers
[issues-shield]: https://img.shields.io/github/issues/mov-cli/mov-cli.svg?style=for-the-badge
[issues-url]: https://github.com/mov-cli/mov-cli/issues
[license-shield]: https://img.shields.io/github/license/mov-cli/mov-cli.svg?style=for-the-badge
[license-url]: https://github.com/mov-cli/mov-cli/blob/master/LICENSE.txt
