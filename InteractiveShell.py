class InteractiveShell(object):
    """This class holds all the interaction methods"""
    def __init__(self, silent):
        super(InteractiveShell, self).__init__()
        self.silent = silent
        self.last_commands = []
        self.exit_commands = ['exit','quit']
        self.create_commands = ['create', 'new']
        self.edit_commands = ['edit', 'update']
        self.delete_commands = ['delete', 'erase']
        self.current_command = ''

    def welcome(self):
        if not self.silent:
            print('Hi, my name is Jane. ' + \
                'I am here to help you create new websites')

    def start_interact(self):
        if not self.silent:
            print('(Jane): What can I do for you? ')
        while self.current_command not in self.exit_commands:
            self.get_user_command()

    def get_user_command(self):
        self.current_command = input('(you): ').lower().strip()
        self.parse_command()

    def parse_command(self):
        if split(self.current_command,' ')[0] in self.known_commands