from FileManager import FileManager

class InteractiveShell(object):
    """This class holds all the interaction methods"""
    def __init__(self, silent, interface):
        super(InteractiveShell, self).__init__()
        self.silent = silent
        self.interface = interface
        self.file_manager = FileManager()
        self.last_commands = []
        self.exit_commands = ['exit','quit','q']
        self.create_commands = ['create', 'start']
        self.edit_commands = ['edit', 'update', 'open', 'use']
        self.delete_commands = ['delete', 'erase']
        self.all_commands = self.exit_commands + self.create_commands + \
                            self.edit_commands + self.delete_commands
        self.ignored_words = ['new']
        self.project_commands = ['project', 'folder', 'repository', 'site']
        self.pages_commands = ['page', 'file', 'stylesheet']
        self.current_command = ''

    def say(self, message):
        if not self.silent:
            if self.interface == 'text':
                print('(Jane): %s ' % message)

    def get_user_command(self):
        if self.interface == 'text':
            self.current_command = self.clean_command(
                input('(you): ').lower().strip())
        self.validate_command()

    def start_interact(self):
        if not self.silent:
            self.say('Hi, my name is Jane. ' + \
                     'I am here to help you create new web sites')
            self.say('What can I do for you?')
        while self.current_command not in self.exit_commands:
            self.get_user_command()

    def validate_command(self):
        split_command = self.current_command.split(' ')
        if split_command[0] in self.all_commands:
            self.last_commands.append(self.current_command)
            self.parse_command(split_command[0], split_command[1:])
        else:
            self.say("Sorry I didn't get what you meant")

    def parse_command(self, cmd, args):
        if cmd in self.create_commands:
            if len(args)>0:
                if args[0] in self.project_commands:
                    if len(args)>1:
                        self.say('I am now creating the project %s' % args[1])
                        self.file_manager.create_project(args[1])
                    else:
                        self.say('How do you want to call this project?')
                elif args[0] in self.pages_commands:
                    pass
                else:
                    self.say("Sorry I didn't get what you want to create")
            else:
                self.say('Do you want to create a new page or a new project?')

    def clean_command(self, cmd):
        split_command = cmd.split(' ')
        for el in self.ignored_words:
            if split_command.count(el)>0:
                split_command.remove(el)
        return ' '.join(split_command)
