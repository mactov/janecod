class InteractiveShell(object):
    """This class holds all the interaction methods"""
    def __init__(self, silent):
        super(InteractiveShell, self).__init__()
        self.silent = silent
        self.last_commands = []
        self.exit_commands = ['exit','quit']
        self.create_commands = ['create', 'start']
        self.edit_commands = ['edit', 'update', 'open', 'use']
        self.delete_commands = ['delete', 'erase']
        self.all_commands = self.exit_commands + self.create_commands + \
                            self.edit_commands + self.delete_commands
        self.ignored_words = ['new']
        self.project_commands = ['project', 'folder', 'repository', 'site']
        self.pages_commands = ['page', 'file', 'stylesheet']
        self.current_command = ''

    def welcome(self):
        if not self.silent:
            print('Hi, my name is Jane. ' + \
                'I am here to help you create new websites')

    def start_interact(self):
        if not self.silent:
            self.ask('What can I do for you?')
        while self.current_command not in self.exit_commands:
            self.get_user_command()

    def get_user_command(self):
        self.current_command = input('(you): ').lower().strip()
        self.clean_command()
        self.validate_command()

    def validate_command(self):
        split_command = self.current_command.split(' ')
        if split_command[0] in self.all_commands:
            self.last_commands.append(self.current_command)
            self.parse_command(split_command[0], split_command[1:])
        else:
            print("(Jane): Sorry I didn't get what you meant")

    def parse_command(self, cmd, args):
        if cmd in self.create_commands:
            if len(args)>0:
                if args[0] in self.project_commands:
                    if len(args)>1:
                        print('I am now creating the new project %s' % args[1])
                    else:
                        self.ask('How do you want to call this project?')
                elif args[0] in self.pages_commands:
                    pass
                else:
                    print("Sorry I didn't get what you want to create")
            else:
                self.ask('Do you want to create a new page or a new project?')

    def clean_command(self):
        split_command = self.current_command.split(' ')
        for el in self.ignored_words:
            if split_command.count(el)>0:
                split_command.remove(el)
        self.current_command = ' '.join(split_command)

    def ask(self, question):
        print('(Jane): %s ' % question)
