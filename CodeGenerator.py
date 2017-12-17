from InteractiveShell import InteractiveShell
from FileManager import FileManager
from WebServer import WebServer
from CommandParser import CommandParser


class CodeGenerator(object):
    
    def __init__(self, silent):
        self.silent = silent
        self.command = ''
        self.action = ''
        self.last_commands = []
        self.parser = CommandParser()
        self.shell = InteractiveShell(
                        self.silent, 'text', self.parser.all_commands())
        self.file_manager = FileManager()
        self.ws = WebServer()
        
    def start(self):
        self.shell.start_interact()
        while not self.parser.is_exit_command(self.command):
            self.command = self.shell.get_user_command()
            if not self.parser.is_valid_command(self.command):
                answer = self.shell.ask(self.parser.get_missing_info())
                self.parser.precise(answer)
            self.action = self.parser.get_action()
            print(self.action)
