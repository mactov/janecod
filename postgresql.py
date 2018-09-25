import psycopg2
from config import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class PSqlCommand:
    def connect(self, dbname):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) = 0 FROM pg_catalog.pg_database"
                        " WHERE datname = '{}'".format(dbname))
            not_exists_row = cur.fetchone()
            not_exists = not_exists_row[0]
            if not_exists:
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cur.execute('CREATE DATABASE {}'.format(dbname))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception('Could not access or create database {}'.format(
                dbname))
        finally:
            if conn is not None:
                conn.close()

