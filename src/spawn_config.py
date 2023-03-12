from typing import Literal, Optional, TypedDict

class PaneConfig(TypedDict):
    path: str
    program: Optional[str]
    split_direction: Optional[Literal["vertical"]|Literal["horizontal"]]

class WindowConfig(TypedDict):
    panes: list[PaneConfig]

class SpawnConfig(TypedDict):
    windows: list[WindowConfig]

