#!/usr/bin/env python

import json
from argparse import ArgumentParser

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
        vertical = pane["split_direction"] == "vertical"
        new_pane = window.split_window(start_directory=pane["path"], vertical=vertical)
        if pane["program"]:
            new_pane.send_keys(pane["program"], enter=True)
        panes.append(new_pane)

    return panes


def get_arguments() -> CLIArguments:
    parser = ArgumentParser()
    parser.add_argument("session_name", type=str)
    parser.add_argument("--config_file", type=str)
    args = parser.parse_args(namespace=CLIArguments())
    return args


def main(session_name: str, config_file: str) -> None:
    server = Server()
    session: Session = server.sessions[0]
    with open(config_file, "r", encoding="utf-8") as o_config_file:
        config: SpawnConfig = json.load(o_config_file)

    windows = create_windows(session, config[session_name])
    for i, window_config in enumerate(config[session_name]):
        create_panes(windows[i], window_config["panes"][1:])


if __name__ == "__main__":
    args = get_arguments()
    main(args.session_name, args.config_file)
