from dataclasses import dataclass


# TODO: ADD EXEPTIONS TO MOODLEAPI
@dataclass
class MoodleException(Exception):
    message: str = ""

    def __str__(self):
        return self.message


@dataclass
class Base(Exception):
    message: str = ""

    def __post_init__(self) -> None:
        self.message = self.message.capitalize()

    def __str__(self):
        return self.message


@dataclass
class RequestException(Exception):
    code: int = 0
    message: str = ""

    def __post_init__(self):
        self.message = f"{self.code} {self.message.capitalize()}"

    def __str__(self):
        return self.message


@dataclass
class DatabaseException(Base):
    message: str = ""


@dataclass
class SecurityException(Base):
    message: str = ""
