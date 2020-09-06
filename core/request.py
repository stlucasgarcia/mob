"""
Requests module responsable to get data from Moodle Platform.
"""

from core.settings import REQUEST

import requests


class Request:
    """Class Request is used for all type of request in API. Be very
    careful with the parameters."""

    def __init__(self, token):
        self.url = REQUEST + token
        self.request = requests


    def __str__(self):
        return f'Request object for {self.url}'


    def get(self, function, *args, **kwargs):
        """GET method recive the function according to func dict in settings.
        All params need to be passed with respectives values well-informed in API"""

        self.url += f'&wsfunction={function}'

        for key, value in kwargs.items():
            self.url += f'&{key}={value}'

        try:
            r = self.request.get(self.url)
            r.raise_for_status()

        except self.request.exceptions.HTTPError as httperror:
            return f'HTTP error occured: {httperror}'

        except Exception as err:
            return f'Other error occured: {err}'

        else:
            return r.json()

    def post(self, *args, **kwargs):
        pass
