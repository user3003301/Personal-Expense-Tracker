from enum import IntEnum, auto, unique

@unique
class ErrorCode(IntEnum):
    SUCCESS = 0
    SRC_NOT_FOUND = auto()
    DST_EXISTS = auto()
    OS_ERROR = auto()