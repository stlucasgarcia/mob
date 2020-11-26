"""
Token module responsible to get users token
"""

from requests import post
from dataclasses import dataclass

from ..security import Cryptography
from ..export import Export, db_exist
from moodleapi.utils import SERVICE, CONNECTION, PLATFORM


@dataclass
class Token:
    """Class Token generates a MoodleAPI token by the user's username and password.
    It also automatically encrypt and storage."""

    url: str = ""
    db_exist("moodle_profile")

    def __str__(self):
        return "Token object"

    def create(self, *args, **kwargs):
        """Create function receive username and password for token creation and additionally
        DiscordID from respective user to be added with the encrypted token in database."""

        url = f"{self.url}{SERVICE}{CONNECTION}{PLATFORM}"
        data = post(url, params=kwargs).json()

        token = Cryptography.encrypt(data["token"])

        inf = [*args[0].values(), token]

        return Export(
            "moodle_profile",
            inf,
        )
