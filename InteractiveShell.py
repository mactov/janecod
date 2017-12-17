class InteractiveShell(object):
    """This class holds all the interaction methods"""
    def __init__(self, silent, interface, commands):
        super(InteractiveShell, self).__init__()
        self.silent = silent
        self.interface = interface
        self.all_commands = commands
        self.ignored_words = {'new'}
        self.current_project = ''
        self.current_page = ''
        self.current_command = ''

    def say(self, message):
        """Displays this message to the user"""
        if not self.silent:
            if self.interface == 'text':
                print('%s(Jane): %s' % (self.prompt(), message))

    def ask(self, question):
        """Asks for more precision"""
        self.say(question)
        return input(self.prompt() + '(you): ').lower().strip()

    def get_user_command(self):
        """Asks the next command to compute"""
        if self.interface == 'text':
            self.current_command = self.clean_command(
                input(self.prompt() + '(you): ').lower().strip())
        self.validate_command()
        return self.current_command

    def start_interact(self):
        """Displays the welcome message"""
        if not self.silent:
            self.say('Hi, my name is Jane. ' + \
                     'I am here to help you create new web sites')
            self.say('What can I do for you?')

    def validate_command(self):
        """Makes sure the current command starts with an appropiate command"""
        split_command = self.current_command.split(' ')
        if not split_command[0] in self.all_commands:
            self.say("Sorry I didn't get what you meant.")

    def clean_command(self, cmd):
        """Removes the ignored words from the command"""
        split_command = cmd.split(' ')
        for el in self.ignored_words:
            if split_command.count(el)>0:
                split_command.remove(el)
        return ' '.join(split_command)

    def prompt(self):
        """Returns the project and page to display at prompt"""
        prompt = ''
        if self.current_project != '':
            prompt = '[' + self.current_project
            if self.current_page != '':
                prompt += '/' + self.current_page
            prompt += ']>'
        return prompt