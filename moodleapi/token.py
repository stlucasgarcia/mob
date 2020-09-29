"""
Token module responsable to get user token (work only once).
"""

from moodleapi.settings import BASEURL
from moodleapi.security import Cryptography
from moodleapi.data.export import Export

from requests import post


class Token:
    """Class Token generate an MoodleAPI token by username and password
    login to automatically encrypt and storage in tokens.csv file."""

    def __init__(self):
        self.post = post
        self.BASEURL = BASEURL
        self.SERVICE = 'login/'
        self.CONNECTION = 'token.php?'
        self.PLATFORM = '&service=moodle_mobile_app'


    def __str__(self):
        return 'Token object creation'


    def create(self, *args, **kwargs):
        """Create function recive username and password for token creation and additionaly
        discordID from respective user to be added with the encrpyted token in csv file."""

        username = f'username={kwargs["username"]}'
        password = f'&password={kwargs["password"]}'

        url = f'{self.BASEURL}{self.SERVICE}{self.CONNECTION}{username}{password}{self.PLATFORM}'
        data = self.post(url).json()


        return Export('moodle_profile').to_db(data=[*args[0].values(), Cryptography().encrypt_message(data['token'])])
