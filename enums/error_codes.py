# Enumeration classes

from enum import IntEnum, auto, unique

@unique
class ErrorCode(IntEnum):
    """Lists the errors that occurred during a renaming operation."""

    SUCCESS = 0
    """Indicates that the operation was successful."""

    SRC_NOT_FOUND = auto()
    """Indicates that the source file was not found."""

    DST_EXISTS = auto()
    """Indicates that the file name destination already exists."""

    OS_ERROR = auto()
    """indicates that an unexpected error has occurred."""