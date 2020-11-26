import logging
from typing import Any

from ..base.process import BaseProcess
from ..core.export import connection, db_exist


class BaseMoodle:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.data: dict = {}
        self.tpool: Any = ""
        self.conn: Any = ""
        self.cursor: Any = ""

    def db(self, db):
        self.tpool, self.conn = connection()
        self.cursor = self.conn.cursor()
        db_exist(db)

    def process_data(self, data, **kwargs):
        self.db(kwargs["db"])
        BaseProcess(
            self.wsfunction,
            data,
            self.cursor,
            self.conn,
            self.token,
            self.r,
            self.url,
            kwargs,
        )
        self.cursor.close()
        self.tpool.putconn(self.conn)
        self.tpool.closeall()
