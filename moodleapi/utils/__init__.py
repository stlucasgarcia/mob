from .request import request

from .settings import (
    functions,
    db_query,
    allowed_modules,
    courses_not_allowed,
    SERVICE,
    CONNECTION,
    PLATFORM,
    month,
    week,
    error_code,
)

from .support import make_params, to_dict

from .version import get_version


class BEX:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\33[31m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


__all__ = [
    # "request", not using for now
    "functions",
    "db_query",
    "allowed_modules",
    "courses_not_allowed",
    "SERVICE",
    "CONNECTION",
    "PLATFORM",
    "month",
    "week",
    "error_code",
    "make_params",
    "to_dict",
    "get_version",
    "BEX",
]
