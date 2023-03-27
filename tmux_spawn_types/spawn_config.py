from typing import Literal, Optional, TypedDict


class PaneConfig(TypedDict):
    path: str
    program: Optional[str]
    split_direction: Optional[Literal["vertical"] | Literal["horizontal"]]


class WindowConfig(TypedDict):
    name: Optional[str]
    panes: list[PaneConfig]


class InstanceConfig(TypedDict):
    windows: list[WindowConfig]
    replace: Optional[bool]


SpawnConfig = dict[str, InstanceConfig]
