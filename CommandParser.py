MISSING_THING = 'What do you want to '
MISSING_NAME = 'How do you want to call it?'

class CommandParser(object):

    def __init__(self):
        self.exit_commands = {'exit','quit','q'}
        self.create_commands = {'create', 'start'}
        self.edit_commands = {'edit', 'update', 'open', 'use'}
        self.delete_commands = {'delete', 'erase'}
        self.project_words = {'project', 'folder', 'repository', 'site'}
        self.page_words = {'page', 'file', 'stylesheet'}
        self.partial_command = ''
        self.action = ''
        self.missing_info = ''

    def is_valid_command(self, cmd):
        spl_cmd = cmd.split(' ')
        if spl_cmd[0] in self.create_commands:
            self.validate_create_command(spl_cmd[1:])
        else:
            pass
        return self.missing_info == ''

    def get_action(self):
        return self.action

    def all_commands(self):
        return self.exit_commands.union(self.create_commands).union(
               self.edit_commands).union(self.delete_commands)

    def is_exit_command(self, cmd):
        return cmd in self.exit_commands

    def get_missing_info(self):
        return self.missing_info

    def precise(self, info):
        self.missing_info = ''
        self.partial_command += ' ' + info
        if self.partial_command.split(' ')[0] in self.create_commands:
            self.validate_create_command(self.partial_command.split(' ')[1:])

    def validate_create_command(self, args):
        if len(args) == 0:
            self.partial_command = 'create'
            self.missing_info = MISSING_THING + 'create ? ' + MISSING_NAME
        else:
            if args[0] in self.project_words:
                self.partial_command = 'create project'
                self.action = 'folder_'
            elif args[0] in self.page_words:
                self.partial_command = 'create page'
                self.action = 'file_'
            else:
                self.missing_info = MISSING_THING + 'create ? '
            if len(args)>1:
                self.missing_info = ''
                self.partial_command = ''
                self.action += args[1]
            else:    
                self.missing_info += MISSING_NAME
