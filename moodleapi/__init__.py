"""
MOODLEAPI PACKAGE FOR CONNECTION WITH THE MOODLE PLATFORM

LATEST VERSION: 4.5.0

STABLE VERSION: 4.5.0
"""


from .mdl import Mdl

from .exception import (
    MoodleException,
    RequestException,
    DatabaseException,
    SecurityException,
)

from .utils import get_version

VERSION = (4, 5, 0)

__version__ = get_version(VERSION)

__all__ = [
    "Mdl",
    "MoodleException",
    "RequestException",
    "DatabaseException",
    "SecurityException",
    "__version__",
]
