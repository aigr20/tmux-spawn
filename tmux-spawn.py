#!/usr/bin/env python

import json
import sys
from argparse import ArgumentParser
from pathlib import Path

from libtmux.pane import Pane
from libtmux.server import Server
from libtmux.session import Session
from libtmux.window import Window

from tmux_spawn_types.cli_arguments import CLIArguments
from tmux_spawn_types.spawn_config import PaneConfig, SpawnConfig, WindowConfig


def create_windows(session: Session, window_config: list[WindowConfig]) -> list[Window]:
    windows: list[Window] = []
    for window in window_config:
        first_pane = window["panes"][0]
        name = None
        if window.get("name") is not None:
            name = window["name"]
        window = session.new_window(
            window_name=name,
            start_directory=first_pane["path"],  # type: ignore because this is typed to always be None for some reason
        )
        windows.append(window)

    return windows


def create_panes(window: Window, config: list[PaneConfig]) -> list[Pane]:
    panes: list[Pane] = []
    for pane in config:
        try:
            vertical = pane["split_direction"] == "vertical"
        except KeyError:
            vertical = True
        new_pane = window.split_window(start_directory=pane["path"], vertical=vertical)
        panes.append(new_pane)
        try:
            if pane["program"]:
                new_pane.send_keys(pane["program"], enter=True)
        except KeyError:
            continue

    return panes


def get_arguments() -> CLIArguments:
    parser = ArgumentParser()
    parser.add_argument("session_name", type=str)
    parser.add_argument("-c", "--config", type=str, help="Use a custom config file")
    parser.add_argument(
        "-r",
        "--replace",
        action="store_true",
        help="Close the current window after opening the session",
    )
    args = parser.parse_args(namespace=CLIArguments())
    return args


def main(arguments: CLIArguments) -> None:
    server = Server()
    session: Session = server.sessions[0]
    try:
        config_f = Path(arguments.config).open(encoding="utf-8")
    except FileNotFoundError:
        print(f"No configuration file at {arguments.config}")
        sys.exit(1)

    try:
        config: SpawnConfig = json.load(config_f)
        config_f.close()
    except json.decoder.JSONDecodeError:
        print("Malformed configuration")
        print(f"Configuration file location: {arguments.config}")
        sys.exit(1)

    initial_window = session.window_active
    spawn_instance = None

    try:
        spawn_instance = config[arguments.session_name]
    except KeyError:
        print(
            f"No window configuration with key {arguments.session_name} found in {arguments.config}"
        )
        sys.exit(1)

    windows = create_windows(session, spawn_instance["windows"])
    for i, window_config in enumerate(spawn_instance["windows"]):
        create_panes(windows[i], window_config["panes"][1:])

    if (arguments.replace and initial_window is not None) or spawn_instance.get(
        "replace"
    ):
        session.kill_window(initial_window)


if __name__ == "__main__":
    args = get_arguments()
    main(args)
