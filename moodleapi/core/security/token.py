"""
Token module responsible to get users token
"""

from dataclasses import dataclass
from requests import post

from ..export import Export
from ..security import Cryptography
from moodleapi.utils import SERVICE, CONNECTION, PLATFORM


@dataclass
class Token:
    """Class Token generate an MoodleAPI token by username and password
    login to automatically encrypt and storage in tokens.csv file."""

    url: str = ""

    def __str__(self):
        return "Token object"

    def create(self, *args, **kwargs):
        """Create function recive username and password for token creation and additionaly
        DiscordID from respective user to be added with the encrpyted token in database."""

        url = f"{self.url}{SERVICE}{CONNECTION}{PLATFORM}"
        data = post(url, params=kwargs).json()

        return Export(
            "moodle_profile",
            [*args[0].values(), Cryptography().encrypt(data["token"])],
        )
