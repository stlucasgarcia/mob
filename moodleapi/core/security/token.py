"""
Token module responsible to get users token
"""

from dataclasses import dataclass
from requests import post

from ..export import Export, create_moodle_profile
from ..security import Cryptography
from moodleapi.utils import SERVICE, CONNECTION, PLATFORM


@dataclass
class Token:
    """Class Token generates a MoodleAPI token by the user's username and password.
    It also automatically encrypt and storage."""

    url: str = ""
    # create_moodle_profile()

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
