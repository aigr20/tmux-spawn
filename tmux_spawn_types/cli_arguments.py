import os
from argparse import Namespace


class CLIArguments(Namespace):
    session_name: str

    def __init__(self) -> None:
        home = os.getenv("HOME")
        xdg_conf_home = os.getenv("XDG_CONFIG_HOME", f"{home}/.config")
        self.config = f"{xdg_conf_home}/tmux-spawn/spawn-config.json"
        self.replace = False
