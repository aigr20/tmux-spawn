from argparse import Namespace


class CLIArguments(Namespace):
    session_name: str

    def __init__(self) -> None:
        self.config_file = "sample-config.json"
