# mov-cli

A cli to browse and watch movies.

## Installation
This project is a work in progress.
However, you can try it out

### python

```python
pip install git+https://github.com/mov-cli/mov-cli
```
### Shell

```bash
sudo curl -s "https://github.com/mov-cli/mov-cli/raw/v3/mov-cli" -L -o /usr/local/bin/mov-cli && sudo chmod +x /usr/local/bin/mov-cli
```

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
For Downloads u need FFmpeg.
For Linux Users: https://ffmpeg.org/download.html#build-linux
For Windows Users: https://github.com/BtbN/FFmpeg-Builds/releases
Linux Users find there Distro and install it.
Windows users need: ffmpeg-master-latest-win64-lgpl.zip and add to path

## Inspiration
Heavily inspired from [ani-cli](https://github.com/pystardust/ani-cli)

## License
[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
