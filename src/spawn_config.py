from typing import Optional, TypedDict

class _Pane(TypedDict):
    path: str
    program: Optional[str]
    split_direction: Optional[str]

class SpawnConfig(TypedDict):
    windows: list[_Pane]

