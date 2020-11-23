import psycopg2
from dataclasses import dataclass

from ..export import search_query
from moodleapi.utils import db_query
from moodleapi.secret import DATABASE


@dataclass
class Export:
    db: str = ""
    data: list = ""

    def __post_init__(self):
        self.conn = psycopg2.connect(**DATABASE)
        self.cursor = self.conn.cursor()
        self.query = search_query(db_query[self.db])
        self._expo()

    def _expo(self):
        self.cursor.execute(self.query, (*self.data,))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
