import typing as tp
import dataclasses
from enum import Enum


class ErrorType(Enum):
    NOERROR = 1
    WARNING = 2
    ERROR = 3
    NOCHECKED = 4
    PROGRAMERROR = 5


@dataclasses.dataclass
class DebugData:
    error_type: ErrorType = ErrorType.NOCHECKED
    error_target_info: tp.Dict[str, int] = dataclasses.field(default_factory=dict)
    # target_objects: tp.List[str] = dataclasses.field(default_factory=list)
    # fix_error_method: tp.Callable = None


@dataclasses.dataclass
class TaskInfo:
    label_name: str = ""
