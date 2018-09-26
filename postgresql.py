import psycopg2
from config import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class PSqlCommand:
    conn = None
    cur = None

    def connect(self, dbname):
        """ Connect to the PostgreSQL database server """
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT COUNT(*) FROM pg_catalog.pg_database "
                             "WHERE datname = '{}'".format(dbname.lower()))
            row = self.cur.fetchone()
            exists = (row[0] > 0)
            if not exists:
                self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                self.cur.execute('CREATE DATABASE {}'.format(dbname.lower()))
            self.cur.close()
            self.conn.close()
            params['database'] = dbname.lower()
            self.conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError):
            raise Exception('Could not access or create database {}'.format(
                dbname))

    def drop_db(self, dbname):
        if self.conn:
            try:
                self.cur = self.conn.cursor()
                self.cur.execute("SELECT COUNT(*) "
                                 "FROM pg_catalog.pg_database "
                                 "WHERE datname = '{}'".format(dbname.lower()))
                row = self.cur.fetchone()
                exists = (row[0] > 0)
                if exists:
                    self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                    self.cur.execute('DROP DATABASE {}'.format(dbname.lower()))
                self.cur.close()
            except (Exception, psycopg2.DatabaseError):
                raise Exception('Could not delete database {}'.
                                format(dbname))

    def drop_all_tables(self):
        if self.conn:
            try:
                self.cur = self.conn.cursor()
                self.cur.execute("SELECT * FROM pg_catalog.pg_tables "
                                 "WHERE schemaname = 'public';")
                rows = self.cur.fetchall()
                if len(rows) > 0:
                    sql = ''
                    for row in rows:
                        sql += 'DROP TABLE {}; '.format(row[1])
                    self.cur.execute(sql)
                self.cur.close()
            except (Exception, psycopg2.DatabaseError) as err:
                print(err)
                raise Exception('Error while deleting tables')

    def create_tables(self, models, drop_all_before=True):
        if drop_all_before:
            self.drop_all_tables()
        # fk = []
        sql = ''
        for mdl in models:
            if mdl['id'] and mdl['fields']:
                sql += "CREATE TABLE {} (id SERIAL PRIMARY KEY, ".format(
                        mdl['id'].lower()
                )
                for fld in mdl['fields']:
                    sql += fld['id'] + ' '
                    ln = fld['length'] if 'length' in fld.keys() else None
                    sql += self.field_type(fld['type'], ln)
                    sql += ' NOT NULL, '  # TODO Remove this hard-coded snippet
                sql = sql[:-2] + ');\n'
        if self.conn and sql:
            try:
                self.cur = self.conn.cursor()
                self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                self.cur.execute(sql)
                self.cur.close()
            except (Exception, psycopg2.DatabaseError):
                raise Exception('Error while writing tables')

    @staticmethod
    def field_type(field_type, field_length):
        s = ''
        if field_type.lower() in ['string', 'char', 'varchar']:
            s += 'VARCHAR('
            if field_length and int(field_length) > 0:
                s += field_length + ')'
            else:
                s += '255)'
        elif field_type.lower() in ['boolean', 'bit']:
            s += 'BOOLEAN'
        elif field_type.lower() in ['integer', 'number', 'foreign_key']:
            s += 'INTEGER'
        elif field_type.lower() in ['real', 'float']:
            s += 'REAL'
        elif field_type.lower() in ['date', 'datetime']:
            s += 'DATETIME'   # TODO Add all data types
        return s

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

