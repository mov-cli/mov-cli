import argparse

args_parser = argparse.ArgumentParser()
args_parser.add_argument("--flatpak-mpv", action = argparse.BooleanOptionalAction)

CMD_ARGS = args_parser.parse_args()
"""Arguments parsed from the command line via argparse."""