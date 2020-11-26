import logging
from typing import Any

from ..base.process import (
    BaseProcess,
)  # TODO: change file name in base module
from ..core.export import connection, db_exist


class BaseMoodle:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.data: dict = {}
        self.tpool: Any = ""
        self.conn: Any = ""
        # self.cursor: Any = ""

    def db(self, db):
        self.tpool, self.conn = connection()
        cursor = self.conn.cursor()
        db_exist(cursor, self.tpool, self.conn, db)
        return cursor

    def process_data(self, data, conn, cursor, **kwargs):
        BaseProcess(
            self.wsfunction,
            data,
            cursor,
            conn,
            self.token,
            self.r,
            self.url,
            kwargs,
        )
