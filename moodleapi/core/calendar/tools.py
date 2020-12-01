from typing import Any
from time import ctime
from re import compile, sub

from moodleapi.utils import week, month
from ..course import simple_contents_information


def clean(value: str) -> str:
    return sub(compile("<.*?>"), "", value)


def time(epoch: int) -> str:
    """Converts the time from epoch to human readable time"""

    date = ctime(epoch).split()

    return f"{week[date[0]]}, {date[2]} de {month[date[1]]} às {date[3][:-3]}"


def verify(r: Any, url: str, token: str, courseid: int, instance: int) -> tuple:
    params = {
        "courseid": courseid,
        "options[0][name]": "cmid",
        "options[0][value]": instance,
        "options[1][name]": "excludecontents",
        "options[1][value]": "True",
    }

    return simple_contents_information(
        r, url, token, "core_course_get_contents", **params
    )
