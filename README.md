# mov-cli
A cli tool to browse and watch movies.

![GitHub Repo stars](https://img.shields.io/github/stars/mov-cli/mov-cli?style=for-the-badge) ![GitHub repo size](https://img.shields.io/github/repo-size/mov-cli/mov-cli?style=for-the-badge) ![GitHub last commit](https://img.shields.io/github/last-commit/mov-cli/mov-cli?style=for-the-badge)

![ezgif com-gif-maker(2)](https://user-images.githubusercontent.com/64269332/183303522-9035eee7-f6a0-4ebe-8d22-753204a64efc.gif)

### Current State
mov-cli doesn´t work, the Providers have changed how they work.
This may take a while to get up and running again.

Sorry, for the inconvenience.

### Python

```python
pip install git+https://github.com/mov-cli/mov-cli
```
### Shell

```bash
sudo curl -s "https://github.com/mov-cli/mov-cli/raw/v3/mov-cli" -L -o /usr/local/bin/mov-cli && sudo chmod +x /usr/local/bin/mov-cli
```

## Usage

### Shell

```bash
mov-cli
```
After running the command, follow the instructions given in your terminal

## Disclaimer
This project is to be used at the user’s own risk, based on their government and laws.

The Devs hold no responsibility for actions done with this Tool.

[Full Disclaimer](disclaimer.org)

## Known issues

```
1. The python version currently doesn't work on some systems(Windows). -> update beautifulsoup4.
2. The read operation timed out. -> fixed.
3. Numbers in titles from actvid, sflix & solar don't show up -> my bad regex. -> fixed.
4. Downloads Don't work. -> fixed.
5. Theflix; no results found. -> fixed
6. Olgply doesn't work.
.
.
.
Many more to be found.
```
*These issues will be fixed soon.*
## Contributing
Pull requests are welcome and *appreciated*. For major changes, please open an issue first to discuss what you would like to change.

## Downloads
```
You'll need FFmpeg, You'll most likely have it if you have mpv installed!
For Linux Users: https://ffmpeg.org/download.html#build-linux
For Windows Users: https://github.com/BtbN/FFmpeg-Builds/releases
IMPORTANT: Please add FFmpeg to Path!!
```
## Inspiration
Heavily inspired from [ani-cli](https://github.com/pystardust/ani-cli)

## License
[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
