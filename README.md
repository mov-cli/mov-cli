<a name="readme-top"></a>

<div align="center">

  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]

  <a href="https://github.com/mov-cli/mov-cli">
    <img src="https://github.com/mov-cli/mov-cli/assets/132799819/a23bec13-881d-41b9-b596-b31c6698b89e" alt="Logo" width="200">
  </a>

  <sub>A cli tool to stream Movies, Tv Shows, LIVE-TV and Anime.</sub>
  <br>
  <br>
  <a href="https://github.com/mov-cli/mov-cli/issues">Report Bug</a>
  ·
  <a href="https://github.com/mov-cli/mov-cli/issues">Request Feature</a>

</div>

<br>

## Installation 🛠️
### Prerequisites
- **[fzf](https://github.com/junegunn/fzf?tab=readme-ov-file#installation)** (optional)
- **[python](https://www.python.org/downloads/)** (required, with pip)
- **[mpv](https://mpv.io/installation/)** (recommended & default media player)

To get running these are all the prerequisites you'll need although you can find some nice extra ones over [here]().

With the prerequisites installed, mov-cli can be installed via the pip command on python versions 3.8 and up.

> [!WARNING]
> As of right now mov-cli **v4** isn't avaible on pip. Use the command below if you would like to install the development version:
> ```sh
> pip install git+https://github.com/mov-cli/mov-cli@v4
> ```

```sh
pip install mov-cli -U
```

## Usage 🖱️
mov-cli comes packaged with a CLI interface via the `mov-cli` command you can use in your respective terminal. 

> [!NOTE]
> You may notice v4 doesn't ship with many scrapers (or previously known as providers) by default, this is because v4 is plugin-based and scrapers are now part of plugins that must be choosen to be installed.
> Find out how to do so at the [wiki](https://github.com/mov-cli/mov-cli/wiki#plugins).

Running the command below will search for `spider man no way home` on the `sflix` scraper.
```sh
mov-cli spider man no way home --provider sflix
```
<img width="370px" src="https://github.com/mov-cli/mov-cli/assets/66202304/86189cab-b246-405e-a266-6c624bee2d36">

<br>

For in-depth instructions hit the wiki: https://github.com/mov-cli/mov-cli/wiki

## Contributing
Pull requests are welcome and *appreciated*. For major changes, please open an issue first to discuss what you would like to change.

<a href = "https://github.com/mov-cli/mov-cli/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=mov-cli/mov-cli"/>
</a>

## Contact
- Author: **Poseidon444** | Discord: ``pain444``
- Maintainer: **R3tr0Ananas** | Discord: ``r3tr0ananas``
- Maintainer: **Goldy** | Discord: ``g0ldy_``

## Inspiration ✨
Heavily inspired from [ani-cli](https://github.com/pystardust/ani-cli)


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
