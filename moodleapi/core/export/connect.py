import psycopg2
from psycopg2 import pool

from moodleapi.secret import DATABASE


def connection():
    """Creates a connection with the database"""

    try:
        threadedpool = psycopg2.pool.ThreadedConnectionPool(1, 20, **DATABASE)

        conn = threadedpool.getconn()

    except (Exception, psycopg2.DatabaseError) as err:
        raise ("Error while connecting to PostgreSQL", err)

    else:
        return threadedpool, conn
