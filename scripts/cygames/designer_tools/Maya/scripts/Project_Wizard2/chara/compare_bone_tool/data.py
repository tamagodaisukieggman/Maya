from enum import Enum
import typing as tp
from dataclasses import dataclass


class CheckState(Enum):
    NO_CHECKED = 0
    HAS_ERROR = 1
    PROG_ERROR = 2
    NO_ERROR = 3
    EXIST_ERROR = 4


@dataclass
class BoneCheckedData:
    joint_name: str = ""
    check_state: CheckState = CheckState.NO_CHECKED
    result = {}
