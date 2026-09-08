#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse
import os

import argcomplete
from Tools import Tools

AVAILABLE_DIR = "/etc/nginx/sites-available"
ENABLED_DIR = "/etc/nginx/sites-enabled"


def get_available_config():
    try:
        return [f for f in os.listdir(AVAILABLE_DIR) if os.path.isfile(os.path.join(AVAILABLE_DIR, f))]
    except FileNotFoundError:
        return []


def get_enabled_config():
    try:
        return os.listdir(ENABLED_DIR)
    except FileNotFoundError:
        return []


def ensite_completer(**kwargs):
    available_config = get_available_config()
    enabled_config = get_enabled_config()
    return [site for site in available_config if site not in enabled_config]


def dissite_completer(**kwargs):
    return get_enabled_config()


def main():
    global AVAILABLE_DIR
    global ENABLED_DIR
    parser = argparse.ArgumentParser()

    sub_parser = parser.add_subparsers(dest="action")
    sub_parser.add_parser("help")
    sub_parser.add_parser("reload")

    parser_ensite = sub_parser.add_parser("ensite", add_help=False)
    parser_ensite.add_argument("config").completer = ensite_completer

    parser_dissite = sub_parser.add_parser("dissite", add_help=False)
    parser_dissite.add_argument("config").completer = dissite_completer

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if not args.action:
        print("No action provided")
        return

    tools = Tools()

    if args.action == "help":
        print("nginx tools v0.1.0-Alpha-dev")

    if args.action == "reload":
        tools.reload()
        return

    if args.action in ["ensite", "dissite"]:
        if not args.config:
            print(f"Error: Path required for '{args.action}'")
            return
        if args.action == "ensite":
            tools.enable_site(args.config, AVAILABLE_DIR, ENABLED_DIR)

        if args.action == "dissite":
            tools.disable_site(args.config, ENABLED_DIR)


if __name__ == "__main__":
    main()
