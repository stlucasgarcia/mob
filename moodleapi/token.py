"""
Token module responsable to get user token.
"""

from moodleapi.settings import BASEURL
from moodleapi.security import Cryptography
from moodleapi.data.export import Export

from requests import post


class Token:
    """Class Token generate an MoodleAPI token by username and password
    login to automatically encrypt and storage in tokens.csv file."""

    def __str__(self):
        return 'Token object'


    @staticmethod
    def create(*args, **kwargs):
        """Create function recive username and password for token creation and additionaly
        DiscordID from respective user to be added with the encrpyted token in database."""

        SERVICE = 'login/'
        CONNECTION = 'token.php?'
        PLATFORM = '&service=moodle_mobile_app'

        username = f'username={kwargs["username"]}'
        password = f'&password={kwargs["password"]}'

        url = f'{BASEURL}{SERVICE}{CONNECTION}{username}{password}{PLATFORM}'
        data = post(url).json()


        return Export('moodle_profile').to_db(data=[*args[0].values(), Cryptography().encrypt_message(data['token'])])
