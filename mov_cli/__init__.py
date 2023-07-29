import argparse

args_parser = argparse.ArgumentParser()
args_parser.add_argument("--flatpak-mpv", action="store_true")
args_parser.add_argument("--vlc", action="store_true")
args_parser.add_argument("--pupdate", action="store_true")
args_parser.add_argument("--debug", action="store_true", required=False)
args_parser.add_argument("-p", required=False, help="Select Provider from Terminal")
args_parser.add_argument("-s", required=False, help="Search from the Terminal")
CMD_ARGS = args_parser.parse_args()

if CMD_ARGS.pupdate:
    from .utils.select import updateProvider

    updateProvider()

"""Arguments parsed from the command line via argparse."""
