import xml.etree.ElementTree as ET


class Project:

    def __init__(self, xml_file):
        self.apps = []
        self.hosts = []
        self.models = []
        self.target = ''
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for child in root:
                if child.tag.lower() == 'target':
                    self.target = child.text.lower()
                elif child.tag.lower() == 'apps':
                    for app in child:
                        self.apps.append(app.text.lower())
                elif child.tag.lower() == 'hosts':
                    for host in child:
                        self.hosts.append(host.text.lower())
                elif child.tag.lower() == 'models':
                    for model in child:
                        self.models.append(self.parse_model(model))
        except IOError:
            print('There has been an error while loading the XML file')

    def parse_model(self, xml_model):
        id = xml_model.attrib['app'].lower() +\
             '_'+xml_model.attrib['name'].lower()
        mdl = {'id': id}
        fields = []
        for field in xml_model:
            if field.tag.lower() == 'field':
                fields.append(field.attrib)
        mdl['fields'] = fields
        return mdl

    def create_sql_db(self):
        pass
