import unittest
from unittest import TestCase

import random
import psycopg2

from moodleapi.secret import DATABASE
from moodleapi.utils import make_params, to_dict, functions


class SupportTestCase(TestCase):
    def setUp(self):
        (
            self.wstoken,
            self.wsfunction,
            self.format,
            self.random_params,
        ) = generate_params()

        self.random_ws_params = generate_ws_params()

    def test_make_params(self):
        self.assertDictEqual(
            make_params(self.wstoken, self.wsfunction, self.format),
            self.random_params,
            "Invalid token, function or format",
        )

    def test_to_dict(self):
        self.assertDictEqual(
            to_dict(self.random_ws_params), self.random_ws_params, "Invalid parameter"
        )


def generate_params():
    conn = psycopg2.connect(**DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT token FROM moodle_profile")

    wstoken = random.choice(cursor.fetchall())
    wsfunction = random.choice(list(functions.keys()))
    moodlewsrestformat = random.choice(["xml", "json"])

    cursor.close()
    conn.close()

    params: dict = {
        "wstoken": wstoken,
        "wsfunction": wsfunction,
        "moodlewsrestformat": moodlewsrestformat,
    }

    return wstoken, wsfunction, moodlewsrestformat, params


def generate_ws_params():
    return random.choice(
        [
            {"categoryid": 2},
            {"day": 30, "month": 9, "year": 2020},
        ]
    )


if __name__ == "__main__":
    unittest.main()
