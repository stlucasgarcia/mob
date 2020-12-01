import unittest
from unittest import TestCase

import convertapi

from moodleapi.core.calendar import clean, time

from .secret import SECRET_KEY


class ToolsTestCase(TestCase):
    def setUp(self):
        generate_text()

    def test_clean(self):
        pass

    def test_time(self):
        pass


def generate_text():
    convertapi.api_secret = SECRET_KEY
    convertapi.convert(
        "txt", {"File": "html_example.txt"}, from_format="html"
    ).save_files("docx_example.txt")


if __name__ == "__main__":
    unittest.main()
