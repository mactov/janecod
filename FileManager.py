import os
from shutil import copyfile


class FileManager(object):
    def __init__(self):
        self.current_project_location = ''
        self.template_folder = os.path.join(os.getcwd(),'templates')

    def create_project(self, name):
        if self.current_project_location == '':
            os.chdir('..')
            folder = os.path.join(os.getcwd(), name)
            if not os.path.isdir(folder):
                os.mkdir(folder)
                self.current_project_location = folder
                self.create_page('index.html', 'empty.html')
                self.create_page('overall.css','empty.css')
                # ws = WebServer(self.current_project_location)
                # ws.start()
                

    def create_page(self, name, template = None):
        if not template == None:
            copyfile(os.path.join(self.template_folder,template), 
                self.current_project_location + '/' + name)