import os

class FileManager(object):
    def __init__(self):
        self.current_project_location = ''

    def create_project(self, name):
        if self.current_project_location == '':
            os.chdir('..')
            folder = os.path.join(os.getcwd(), name)
            if not os.path.isdir(folder):
                os.mkdir(folder)
                self.current_project_location = folder