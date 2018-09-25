import xml.etree.ElementTree as et


class Project:
    target = ''
    hosts = []
    name = ''
    apps = []
    models = []

    def __init__(self):
        self.load_from_xml('meta.xml')

    def create_sql(self):
        if self.models:
            print(self.models)

    def load_from_xml(self, xml_file):
        try:
            tree = et.parse(xml_file)
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

    @staticmethod
    def parse_model(xml_model):
        _id = xml_model.attrib['app'].lower() + \
             '_' + xml_model.attrib['name'].lower()
        mdl = {'id': _id}
        fields = []
        for field in xml_model:
            if field.tag.lower() == 'field':
                fields.append(field.attrib)
        mdl['fields'] = fields
        return mdl
