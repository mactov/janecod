import psycopg2
from config import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class PSqlCommand:
    conn = None
    cur = None
    dbname = ''

    def connect(self, dbname, delete_db_if_exists=True):
        """ Connect to the PostgreSQL database server """
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            if delete_db_if_exists:
                self.cur.execute('DROP DATABASE IF EXISTS {};'.
                                 format(dbname.lower()))
            self.cur.execute("SELECT COUNT(*) FROM pg_catalog.pg_database "
                             "WHERE datname = '{}'".format(dbname.lower()))
            row = self.cur.fetchone()
            exists = (row[0] > 0)
            if not exists:
                self.cur.execute('CREATE DATABASE {};'.format(dbname.lower()))
            self.cur.close()
            self.conn.close()
            self.dbname = dbname
            params['database'] = self.dbname.lower()
            self.conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)
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
                    self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                    self.cur.execute(sql)
                self.cur.close()
            except (Exception, psycopg2.DatabaseError) as err:
                print(err)
                raise Exception('Error while deleting tables')

    def create_tables(self, models, drop_all_before=True,
                      prepend_app_name=True):
        if drop_all_before:
            self.connect(self.dbname, True)
        sql_create = ''
        sql_fk = ''
        for mdl in models:
            if mdl['id'] and mdl['fields']:
                if mdl['app'] and prepend_app_name:
                    table_name = mdl['app'].lower() + '_' + mdl['id'].lower()
                else:
                    table_name = mdl['id'].lower()
                sql_create += "CREATE TABLE {} (id SERIAL PRIMARY KEY, ".\
                              format(table_name)
                for fld in mdl['fields']:
                    sql_create += fld['id'] + ' '
                    ln = fld['length'] if 'length' in fld.keys() else None
                    sql_create += self.field_type(fld['type'], ln)
                    if fld['type'].lower() in ['foreign_key',
                                               'foreign key', 'fk']:
                        rel_app = fld['related_app'] if \
                                  'related_app' in fld.keys() else mdl['app']
                        sql_fk += self.add_fk(mdl['app'], mdl['id'], fld['id'],
                                              rel_app, fld['related_model'])
                    if 'nullable' in fld.keys() and\
                            fld['nullable'].lower() in ['false', 'no', '0']:
                        sql_create += ' NOT NULL'
                    if 'default' in fld.keys() and fld['default']:
                        sql_create += ' DEFAULT {}'. format(fld['default'])
                    sql_create += ','
                sql_create = sql_create[:-1] + ');\n'
        sql = sql_create + sql_fk
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

    @staticmethod
    def add_fk(app_from, table_from, field_from,
               app_to, table_to, prepend=True):
        if prepend:
            tf = app_from.lower() + '_' + table_from.lower()
            tt = app_to.lower() + '_' + table_to.lower()
        else:
            tf = table_from.lower()
            tt = table_to.lower()
        return "ALTER TABLE {} ADD CONSTRAINT {} FOREIGN KEY ({}) REFERENCES" \
               " {} (id);".format(tf, tf + '_to_' + tt, field_from, tt)

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

