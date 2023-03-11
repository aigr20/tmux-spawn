#!/usr/bin/env python

import json
from pprint import pprint

from libtmux.server import Server

from src.spawn_config import SpawnConfig


def main() -> None:
    server = Server()
    session = server.sessions[0]
    with open("sample-config.json", "r", encoding="utf-8") as config_file:
        config: SpawnConfig = json.load(config_file)
    pprint(config)

if __name__ == "__main__":
    main()
