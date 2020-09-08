"""
Token module responsable to get user token (work only once).
"""

from moodleapi.settings import BASEURL
from moodleapi.security import Cryptography
from moodleapi.data.export import Export

from requests import post


class Token:

    def __init__(self):
        self.post = post
        self.BASEURL = BASEURL
        self.SERVICE = 'login/'
        self.CONNECTION = 'token.php?'
        self.PLATFORM = 'service=moodle_mobile_app'


    def __str__(self):
        return 'Token object creation'


    def create(self, username=None, password=None, discordid=None, *args, **kwargs):
        username = f'&username={username}'
        password = f'&password={password}'

        url = f'{self.BASEURL}{self.SERVICE}{self.CONNECTION}{username}{password}{self.PLATFORM}'
        data = self.post(url).json()
        print(data)



        return Export('tokens.csv').to_csv(data=[[Cryptography().encrypt_message(data), discordid],], addstyle=True)
