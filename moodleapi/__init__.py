"""
MOODLEAPI PACKAGE FOR CONNECTION WITH MOODLE PLATFORM

LATEST VERSION: 4.2.0

STABLE VERSION: 4.2.0
"""


from .mdl import Mdl

from .exception import (
    MoodleException,
    RequestException,
    DatabaseException,
    SecurityException,
)

from .utils import get_version

VERSION = (4, 2, 0, "f")

__version__ = get_version(VERSION)

__all__ = [
    "Mdl",
    "MoodleException",
    "RequestException",
    "DatabaseException",
    "SecurityException",
]
