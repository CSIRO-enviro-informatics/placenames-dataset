from .secrets import DB_HOST, DB_PORT, DB_DBNAME, DB_USR, DB_PWD  # the secrets from the secret config file

import psycopg2  # installed with LDFLAGS=-L/usr/local/opt/openssl/lib pip install psycopg2
import psycopg2.extras


connect_str = "host='{}' port='{}' dbname='{}' user='{}' password='{}'"\
    .format(DB_HOST, DB_PORT, DB_DBNAME, DB_USR, DB_PWD)


def db_select(q):
    try:
        conn = psycopg2.connect(connect_str)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(q)
        return cur.fetchall()
    except Exception as e:
        print(e)
