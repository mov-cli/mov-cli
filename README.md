<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/mov-cli/mov-cli">
    <img src="https://github.com/mov-cli/mov-cli/assets/132799819/a23bec13-881d-41b9-b596-b31c6698b89e" alt="Logo" width="80" height="80">
  </a>

  <p align="center">
    Welcome to mov-cli! A CLI tool to browse and watch Movies, Shows, TV, and Sports.
    <br />
    <br />
    <a href="https://github.com/mov-cli/mov-cli/issues">Report a Bug</a>
    ·
    <a href="https://github.com/mov-cli/mov-cli/issues">Request a Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
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
        <li><a href="#windows">Windows</a></li>
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
  <li><a href="#inspiration">Inspiration</a></li>
</ol>


<!-- ABOUT THE PROJECT -->
## About The Project

Welcome to the new and improved mov-cli!

mov-cli is your go-to Commandline Tool for streaming and downloading your favorite shows and movies.

Shows and movies are sourced from various streaming sites.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started



### Prerequisites

To get started, make sure you have the following installed:

- [`mpv`](https://mpv.io) - Player for Windows, Linux, and Android
- [`iina`](https://iina.io) - Player for MacOS
- [`Outplayer`](https://outplayer.app/) - Player for iOS
- [`ffmpeg`](https://github.com/FFmpeg/FFmpeg) - Media encoder
- [`fzf`](https://github.com/junegunn/fzf) - Selection Menu


## Installation
<!-- WINDOWS -->
### Windows
(Recommended) Run the following commands (including mov-cli) on any Windows system using the latest modern build version of cmd from the Microsoft Store: [terminal](https://apps.microsoft.com/detail/9n0dx20hk701?hl=en-us&gl=US)
  - Run as admin:
    ``` 
    powershell -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"  
    ```
  - Restart cmd as admin, then run:
    ```
    choco install -y fzf ffmpeg-full python3 mpv
    ```
  - Restart cmd as admin again, then:
    ```
    pip3 install mov-cli
    ```
  - Optional:
    ```
    pip install lxml
    ```
<!-- LINUX -->
### Linux
We offer MPR and AUR Builds for Linux.

- [MPR Build](https://mpr.makedeb.org/packages/mov-cli)
- [AUR Build](https://aur.archlinux.org/packages/mov-cli-git)

#### Disclaimer: These builds are not maintained by us.


<!-- ANDROID --> 
### Android               
Ensure you have [[MPV Android](https://play.google.com/store/apps/details?id=is.xyz.mpv) | [Termux](https://f-droid.org/en/packages/com.termux/)] installed on Android prior to mov-cli installation!
  - In Termux, run the following commands:
    ```
    termux-setup-storage
    yes | pkg update && pkg upgrade && yes | pkg install fzf ffmpeg python && pip3 install mov-cli
    ```
  then run mov-cli a cuple of times before useing it normally.
  - Optional
    ```
    apt-get install libxml2 libxslt
    pip install lxml
    ```


<!-- IOS -->
### iOS
   Make sure [[Outplayer](https://apps.apple.com/us/app/outplayer/id1449923287) | [iSH](https://apps.apple.com/us/app/ish-shell/id1436902243)] are installed.
   - Run the following commands (Note: this may take a while)
   ```
   apk update && apk upgrade
   apk add python3 fzf
   python3 -m ensurepip
   mkdir /home/root && mkdir /home/root/.config
   pip3 install mov-cli
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

You can type ```mov-cli``` in to youre terminal without any arguments
  - Usage:
  ```
  mov-cli [-p 'providername' , -s 'search query' , --pupdate]
    -p : for atomaticaly selecting the provider by typing its name out, skipping the provider selection menue.
    -s : search query for the selected provider, ether prior to provider selection or after if -p was passed.
    --pupdate : (provider update) used for provider urls addreses update, used if a provider not responding by defult urls in mov-cli.
  
  example:
    mov-cli -p sflix -s "spider man"  :  will have mov-cli auto select sflix as youre provider and start searching
                                         for "spider man" on sflix and return a list
  ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>
 
<!-- ON UPDATE -->
## On update
When you update the package, please delete the appdata folders:
### On Windows

It is located at
```
{home}/AppData/Roaming/mov-cli
```
### On Linux

It is located at
```
/home/{getuser()}/.config/mov-cli
```
### On Android

It is located at
```
/data/data/com.termux/files/home
done by typing in termux:
yes | rm -r mov-cli/
```
### On iOS

It is located at
```
/root/mov-cli_config
```
### On Darwin

It is located at
```
/Users/{getuser()}/Library/Application Support/mov-cli
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DISCLAIMER -->
## Disclaimer

**Disclaimer:**
Usage of this software is entirely at your own discretion and risk. Users are advised to comply with their government's laws and regulations regarding content consumption.
We do not exercise control over the content served through this software. Any copyrighted material accessed is the sole responsibility of the user.

**Legal Compliance:**
Users are encouraged to respect intellectual property rights and comply with applicable copyright laws. The developer cannot be held liable for any unauthorized usage of copyrighted content.

---
[More on this](https://github.com/mov-cli/mov-cli/blob/v3/disclaimer.org)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Feature -->
## Feature

If you want a feature, create an [issue](https://github.com/mov-cli/mov-cli/issues/new) or create the feature and make a pull request.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing


Pull requests are welcome and _appreciated_. For major changes, please open an issue first to discuss what you would like to change.

Contributors:

<a href = "https://github.com/mov-cli/mov-cli/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=mov-cli/mov-cli"/>
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Author: Poseidon444 | ```Discord: pain444```

Maintainer: HLOAnanas | ```Discord: r3tr0ananas```

Project Link: [https://github.com/mov-cli/mov-cli](https://github.com/mov-cli/mov-cli)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Inspiration -->
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
