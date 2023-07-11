import argparse

args_parser = argparse.ArgumentParser()
args_parser.add_argument("--flatpak-mpv", action=argparse.BooleanOptionalAction)
args_parser.add_argument("-p", required=False, help="Select Provider from Terminal")
args_parser.add_argument("-s", required=False, help="Search from the Terminal")
CMD_ARGS = args_parser.parse_args()

"""Arguments parsed from the command line via argparse."""