import unittest
from unittest import TestCase

import psycopg2
import random

from moodleapi.core.export import search_query
from moodleapi.secret import DATABASE

from tests.unit_tests.export_tests import query_dict


class DatabaseTestCase(TestCase):
    def setUp(self):
        self.db_name, self.random_query = pick_random_query()

    def test_search_query(self):
        self.assertEqual(
            search_query(self.db_name), self.random_query, "The query is different"
        )


def pick_random_query():
    conn = psycopg2.connect(**DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='public' "
        "AND table_type='BASE TABLE';"
    )

    db = random.choice(cursor.fetchall())[0]
    query = query_dict[f"{db}_query"]

    cursor.close()
    conn.close()

    return db, query


if __name__ == "__main__":
    unittest.main()
