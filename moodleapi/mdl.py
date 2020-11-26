from typing import Any
from requests import Session
from dataclasses import dataclass

from .base import BaseMoodle
from .utils import make_params, to_dict


@dataclass
class Mdl(BaseMoodle):  # TODO: add description to classes and functions
    r: Any = Session()

    def __call__(self, token: str, url: str, wsfunction: str):
        super().__init__()
        self.token = token
        self.url = url
        self.wsfunction = wsfunction

    def get(self, moodlewsrestformat="json", **kwargs):
        params = make_params(self.token, self.wsfunction, moodlewsrestformat)
        params.update(to_dict(kwargs))
        r = self.r.get(self.url, params=params, stream=True)
        if r.ok and moodlewsrestformat == "json":
            self.data = r.json()

    def export(self, **kwargs):
        self.process_data(self.data, **kwargs)
