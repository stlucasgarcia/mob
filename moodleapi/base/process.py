from typing import Any
from dataclasses import dataclass

import colorama
from colorama import Fore, Style

from ..utils import (
    functions,
    courses_not_allowed,
    allowed_modules,
    error_code,
)

from ..core.export import (
    search_query,
    events_check,
)

from ..core.calendar import (
    upcoming_information,
    upcoming_check_information,
)

from moodleapi.exception import MoodleException


@dataclass
class BaseProcess:
    wsfunction: str = ""
    data: dict = ""
    cursor: Any = ""
    conn: Any = ""
    token: str = ""
    r: Any = ""
    url: str = ""
    kwargs: dict = ""

    def __post_init__(self):
        if self._process_response():
            getattr(self, functions[self.wsfunction])()

    def _process_response(self):
        if "exception" in self.data.keys():  # TODO: REVISE
            colorama.init()
            print(
                MoodleException(
                    f"{Fore.RED}moodle.exception.MoodleException: "
                    f"An error occured while connecting with MoodleAPI -> "
                    f"{Style.BRIGHT}{self.data['message']}{Style.NORMAL} "
                    f"{Fore.LIGHTBLACK_EX}(error code: {error_code[self.data['errorcode']]}){Style.RESET_ALL}"
                )
            )
            return False

        else:
            return True

    def monthly(self):
        pass

    def upcoming(self):
        events = self.data["events"]
        query = search_query(self.kwargs["db"])

        if self.kwargs["db"] == "moodle_assign":
            events_check(
                self.cursor,
                self.conn,
                "moodle_assign",
                self.kwargs["discord_id"],
                self.kwargs["guild_id"],
            )

            for event in events:
                if (
                    event["course"]["id"] not in courses_not_allowed
                    and event["modulename"] in allowed_modules
                ):

                    params = {
                        "course": self.kwargs["course"],
                        "semester": self.kwargs["semester"],
                        "class": self.kwargs["clss"],
                        "subject": event["course"]["fullname"],
                        "guild_id": self.kwargs["guild_id"],
                        "token": self.token,
                        "courseid": event["course"]["id"],
                        "cursor": self.cursor,
                        "conn": self.conn,
                        "r": self.r,
                        "url": self.url,
                    }

                    self.cursor.execute(
                        query,
                        (
                            self.kwargs["discord_id"],
                            self.kwargs["guild_id"],
                            self.kwargs["course"],
                            self.kwargs["semester"],
                            self.kwargs["clss"],
                            *upcoming_check_information(
                                event["course"]["fullname"],
                                event["name"],
                                event["description"],
                                event["modulename"],
                                event["formattedtime"],
                                event["url"],
                                event["course"]["id"],
                                event["instance"],
                                params,
                            ),
                        ),
                    )
                    self.conn.commit()

        else:
            events_check(
                self.cursor,
                self.conn,
                "moodle_events",
                self.kwargs["discord_id"],
                self.kwargs["guild_id"],
            )

            for event in events:
                if (
                    event["course"]["id"] not in courses_not_allowed
                    and event["modulename"] in allowed_modules
                ):

                    params = {
                        "course": self.kwargs["course"],
                        "semester": self.kwargs["semester"],
                        "class": self.kwargs["clss"],
                        "subject": event["course"]["fullname"],
                        "guild_id": self.kwargs["guild_id"],
                        "token": self.token,
                        "courseid": event["course"]["id"],
                        "cursor": self.cursor,
                        "conn": self.conn,
                        "r": self.r,
                        "url": self.url,
                    }

                    self.cursor.execute(
                        query,
                        (
                            self.kwargs["discord_id"],
                            self.kwargs["guild_id"],
                            self.kwargs["course"],
                            self.kwargs["semester"],
                            self.kwargs["clss"],
                            *upcoming_information(
                                event["course"]["fullname"],
                                event["name"],
                                event["description"],
                                event["modulename"],
                                event["formattedtime"],
                                event["url"],
                                params,
                            ),
                        ),
                    )
                    self.conn.commit()

    def day(self):  # TODO: Redirecting to upcoming
        if self.kwargs["db"] in ("moodle_events", "moodle_assign"):
            self.upcoming()

        else:
            pass

    def contents(self):
        if self.kwargs["option"] == "contents":
            pass

        elif self.kwargs["option"] == "simple":
            pass

        elif self.kwargs["option"] == "professor":
            pass

    def courses(self):
        pass
