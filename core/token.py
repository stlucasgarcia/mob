"""
Token module responsable to get user token (work only once).
"""

from requests import post
from core.settings import BASEURL


class Token:

    def __init__(self):
        self.post = post
        self.BASEURL = BASEURL
        self.SERVICE = 'login/'
        self.CONNECTION = 'token.php?'
        self.PLATFORM = 'service=moodle_mobile_app'

    def __str__(self):
        return 'Token request object'

    def post(self, username=None, password=None, *args, **kwargs):
        username = f'&username={username}'
        password = f'&password={password}'

        url = f'{self.BASEURL}{self.SERVICE}{self.CONNECTION}{self.PLATFORM}{username}{password}'
        data = self.post(url).json()

        return data['token']
