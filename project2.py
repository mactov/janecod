from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

class Project:
    target = 'sql'
    hosts = ['localhost']
    credentials = {'host': 'localhost', 'port': '5432', 'user': 'mactov', 'pass': 'Natika091076'}
    name = 'ERP'
    apps = ['CRM']
    models = [{'id': 'crm_customer',
                    'fields': [
                        {'name': 'name', 'type': 'string'},
                        {'name': 'is_company', 'type': 'boolean'}]},
                   {'id': 'crm_contact',
                    'fields': [
                        {'name': 'first_name', 'type': 'string'},
                        {'name': 'last_name', 'type': 'string'},
                        {'name': 'customer', 'type': 'foreign_key'}]}
                   ]

    def create_sql(self):
        #this has nothing to do with sql alchemy, that is an ORM, but with psycopg only
        #it is only a matter of generating CREATE TABLE in the appropriate order

        url = 'postgres://{0}:{1}@{2}:{3}/{4}'.format(self.credentials['user'], self.credentials['pass'], self.hosts[0],
                                                      self.credentials['port'], self.name)
        engine = create_engine(url, echo=True)
        if not database_exists(engine.url):
            create_database(engine.url)

        if self.models:
            for m in self.models:
                print(m['id'])

    def render_models(self):
        for mdl in self.models:
            maxl = 0
            if mdl['id'] > maxl:
                maxl = mdl['id']

    def print_model(self, width, model_name, field_names):
        pass

    def print_line(self, width):
        pass

    def print_name(self, width, name):
        pass