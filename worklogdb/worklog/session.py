import re
import collections
import sys

from worklogdb.worklog.models import Employee
from worklogdb.worklog.helpers import clear, get_input, quit
RC_RETURN = 'return'


class Session:
    user = None

    def __init__(self):
        self.mainmenu = collections.OrderedDict([
            ('q', (quit, '')),
            ('a', (self.add_logentry, '')),
            ('v', (self.view_own_entries, '')),
            ('a', (self.view_all_entries, '')),
        ])

    def login_dialog(self):
        loginmenu = collections.OrderedDict([
            ('l', (self.login, 'Please enter your first name\n> ')),
            ('r', (self.register, 'Please register')),
        ])
        self.dialog(menu=loginmenu)
        print("Hello {}, you are now logged in".format(self.user))

    def dialog(self, menu, rc_finish=None):
        """Show the menu"""
        menu['q'] = (quit, '')
        header = 'Welcome to the Weblog Application'
        nextstep = None
        msg, err_msg = None, None
        kwargs = {}
        while nextstep != RC_RETURN:
            print(nextstep)
            # screen is cleared
            clear()

            # print header and menu
            print("{0}\n{1}\n{0}".format(60 * '=', header))
            for key, value in menu.items():
                print('{}) {}'.format(key, value[0].__doc__))

            # print last received error message
            if err_msg:
                print("{0}\n{1}\n{0}".format(60 * '=', err_msg))
                err_msg = None

            # if there is no last message set, use default
            msg = msg or 'Please choose and action\n>'

            # receiving userinput
            userinput = input('{} '.format(msg)).strip()

            # process userinput
            choice = userinput.lower()
            kwargs['userinput'] = userinput
            try:
                #import pdb;
                #pdb.set_trace()
                if choice in menu:
                    choice_func = menu[choice][0]
                    if choice_func == quit:
                        quit()
                    elif choice_func == self.login:
                        nextstep, msg = self.login(**kwargs)
                    elif choice_func == self.register:
                        nextstep, msg = self.register(**kwargs)
                elif nextstep:
                    if nextstep == self.get_employee_list:
                        nextstep, msg, employee_list\
                            = self.get_employee_list(**kwargs)
                        if employee_list:
                            kwargs['employee_list'] = employee_list
                    elif nextstep == self.login_from_list:
                        nextstep, msg, user = self.login_from_list(**kwargs)
                        if user:
                            self.user = user
                    elif nextstep == self.create_employee:
                        nextstep, msg, user\
                            = self.create_employee(**kwargs)
                        if user:
                            self.user = user
            except DialogError as e:
                err_msg = e

    def login(self, **kwargs):
        """login"""
        msg = 'Please type in your first name\n> '
        return self.get_employee_list, msg

    def get_employee_list(self, **kwargs):
        """check firstname and return all employees with that name as a list to choose from."""
        userinput = kwargs.pop('userinput', '')
        if userinput == '':
            raise DialogError('No name received.')
        else:
            userinput = userinput.capitalize()
            firstname_pattern = r'(?P<first_name>^[\w]+$)'
            match = re.match(firstname_pattern, userinput)
            if match and match.group('first_name'):
                firstname = match.group('first_name')
            else:
                raise DialogError('{} is not a valid first name.'.format(userinput))
            employee_list = \
                list(Employee.select().where(Employee.first_name == firstname))
            msg = "This is what we have on file for '{}':\n".format(firstname)
            if employee_list:
                for employee in employee_list:
                    msg += "[{}] {}\n".format(employee_list.index(employee) + 1, employee)
                msg += ("\nPlease choose from the employee list by number\n"
                        "or type [r]egister, if none of these are you\n> ")
                return self.login_from_list, msg, employee_list
            else:
                msg = ("We could not find anybody with first name '{}'.\n"
                       "Did you misspell your name?\n"
                       "Try again or register with [r]!\n> ".format(userinput))
                return self.get_employee_list, msg, None


    def login_from_list(self, *args, **kwargs):
        """check choice from list and return active employee instance"""
        employee_list = kwargs.pop('employee_list', None)
        userinput = kwargs.pop('userinput', None)
        try:
            index = int(userinput) - 1
            user = employee_list[index]
            msg = ("Hello {}, you are now logged in.")
        except [ValueError, IndexError]:
            raise DialogError('{} is not a valid row number')
        else:
            return RC_RETURN, msg, user

    def register(self, **kwargs):
        """register """
        msg = ("Please register with your first and last"
               "name, such as: 'Mickey Mouse'\n> ")
        return self.create_employee, msg

    def create_employee(self, **kwargs):
        """check full name input and create employee"""
        userinput = kwargs.pop('userinput', '')
        if userinput == '':
            raise DialogError('No name received.')
        fullname_pattern \
            = r'(?P<first_name>^[\w]+)([\s]*(?P<last_name>[\w]+$))'
        userinput.strip()
        match = re.match(fullname_pattern, userinput)
        if match:
            first_name = match.group('first_name').capitalize()
            last_name = match.group('last_name').capitalize()
            employee = Employee.create(first_name=first_name, last_name=last_name)
            msg = "Welcome {}, you account has been created".format(self.user)
            return RC_RETURN, msg, employee
        else:
            raise DialogError("{} is not a valid name.".format(userinput))

    def add_logentry(self):
        """Add logentry"""
        print('you can now enter a logentry')

    def view_own_entries(self):
        """View your own logentries"""
        print('you can now view your own entries')

    def view_all_entries(self):
        """View other logentries"""
        print('you can now view all entries')

class DialogError(Exception):
    pass
