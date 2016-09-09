"""
This file contains the Base Dialog Class
"""
import sys
from collections import OrderedDict, namedtuple
from worklogdb.worklog.helpers import quit, clear

DialogStep = namedtuple('DialogStep',
                        ['checkinput_func',
                         'process_func',
                         'prompt',
                         'input_method'])
DialogStep.__new__.__defaults__ = (None, None, '', input)
ReturnCode = namedtuple('ReturnCode', ['okay', 'quit_dialog', 'data', 'msg'])
ReturnCode.__new__.__defaults__ = (False, False, None, '')
ChoiceList = namedtuple(
    'ChoiceList',
    ['list',
     'name',
     'choice_func',
     'choice_process_func',
     'fmt_func',
     'fmt_detail_func'])
ChoiceList.__new__.__defaults__ = \
    (None, '', None, None, lambda x: x, lambda x: x)


class BaseDialog:
    """
    The base dialog is a dialog skeleton that is used by
    all the other dialogs. Its core is the dialog loop in the main method.
    It offers a choice list: if choice is set to true the user can choose
    from a list and then the active choice item and index are set.
    """
    def __init__(self):
        """
        the dialog is initialized
        """
        self.msg = None
        self.choice = None
        self.choice_list = None
        self.active_choice_item = None
        self.active_choice_index = None
        self.quit_dialog = False
        self.return_msg = None
        self.title = ""

    def main(self):
        """
        the main loop consists of the following parts:
        - when 'q' is chosen or the dialog is set to quit: it escapes
        the loop
        - otherwise the screen is printed
        - the input method and the prompt are fetched from the dialog step
        - the userinput is processed
        - it is checked whether the dialogs goal is reached
        - if the dialog is set to quit: the retunr parameters are set
        """
        menuchoice = None
        self.init_main()
        while menuchoice != 'q' and not self.quit_dialog:

            self.print_screen()

            inputmethod, prompt = self.get_method_and_prompt()
            userinput = inputmethod(prompt)

            self.process_userinput(userinput)
            self.check_for_dialog_goal()
            if self.quit_dialog:
                return self.get_return_parameters()

    def check_for_dialog_goal(self):
        """
        this function is overwritten by the dialogs as needed:
        it checks whether a dialogs goal has been reached.
        """
        pass

    def get_return_parameters(self):
        """
        the dialog returns a message to the caller,
        this method can be overwritten to return other data
        """
        return self.return_msg

    def init_main(self):
        """
        the main loop is initialized by setting up the menu
        and fetching the first dialogstep
        """
        self.menu = self.get_menu()
        self.activestep = self.get_first_dialogstep()

    def print_screen(self):
        """
        the screen is cleared, the next menu is fetched and
        the user receives a new print out in each loop
        """
        clear()
        self.menu = self.update_menu()
        self.print_data()

    def process_userinput(self, userinput):
        """
        the userinput id processed.
        - it is generally stripped
        - it is tested against the menu which generally takes priority
        - it is expected that the user has taken a menu choice or
          the userinput can be input for a dialogstep if there is an active
          dialog step or it can be a choice in a list, if choice is true.
          in case none of these conditions are true,
          the user receives a message
        - in case of a choice: the userinput is tested,
          whether it is a valid row
        - in both cases choice and activestep: the inputcheck returns a
          process_func if the check went okay. This process function
          is performed after the check went through and may set the dialog
          to quit in which case a message may be returned
        """
        userinput = userinput.strip()
        menuchoice = userinput.lower()

        if menuchoice in self.menu:
            print(self.menu[menuchoice])
            self.menu[menuchoice]()
            print(self.update_menu)
            self.update_menu()
            return

        if not (self.choice or self.activestep):
            self.msg = '{} is no valid menu choice'.format(menuchoice)
            return

        else:
            process_func = None
            if self.choice:
                if not self.check_valid_choice_list_index(userinput):
                    return
                if self.choice_list.choice_func:
                    process_func = self.choice_list.choice_func()
            else:
                process_func = self.activestep.checkinput_func(userinput)
            if process_func:
                self.msg = process_func()
                if self.quit_dialog:
                    return self.msg

    def get_first_dialogstep(self):
        """
        get the first dialogstep: this function is overwritten by the dialogs
        """
        return None

    def update_menu(self):
        """
        update the menu: some dialogs update their menu for each loop
        """
        return self.get_menu()

    def check_valid_choice_list_index(self, userinput):
        """
        when the userinput was a choice in a list:
        check whether it is a valid row number
        """
        try:
            index = int(userinput) - 1
            self.active_choice_item = self.choice_list.list[index]
        except ValueError:
            self.msg = '{} is not a number'.format(userinput)
        except IndexError:
            self.msg = '{} is not a valid row number'.format(userinput)
        else:
            self.active_choice_index = index
            self.choice = False
            return True

    def build_print_data(self):
        """
        build a stack for print
        """
        print_stack = []
        print_stack.append("=" * 60)
        print_stack.append("Worklog Application:\n>> {}".format(self.title))
        print_stack.append("=" * 60)
        for key, value in self.menu.items():
            print_stack.append('{}) {}'.format(key, value.__doc__))
        if self.choice:
            print_stack.append("-" * 60)
            for row in self.choice_list.list:
                print_stack.append(
                    "[{}] {}"
                    .format(
                        self.choice_list.list.index(row) + 1,
                        self.choice_list.fmt_func(row))
                )
        else:
            print_stack.append("-" * 60)
            if self.active_choice_item:
                row_nr = "[{}] ".format(self.active_choice_index + 1)
                print_stack.append(
                    row_nr +
                    self.choice_list.fmt_detail_func(self.active_choice_item)
                )
        if self.msg:
            print_stack.append(self.msg)
            self.msg = None
            print_stack.append("-" * 60)
        self.add_to_print_stack(print_stack)
        return print_stack

    def add_to_print_stack(self, print_stack):
        """
        add to the print stack: this method can be overwritten by the dialogs
        to print extra stuff
        """
        pass

    def print_data(self):
        """
        print the data from the print stack
        """
        print_stack = self.build_print_data()
        for line in print_stack:
            print(line)

    def back(self):
        """back"""
        self.quit_dialog = True

    def get_menu(self):
        """
        fetches the initial menu
        """
        return OrderedDict([
            ('b', self.back),
            ('q', quit),
        ])

    def get_method_and_prompt(self):
        """
        get prompt amd method for the userinput:
        - there is a default prompt
        - there is a prompt for choice in a list
        - otherwise the activestep knows its prompt and input method
        """
        if self.choice:
            return self.get_input_with_input, \
                   "{}> ".format('Please choose a row number')
        elif self.activestep:
            if self.activestep.input_method == input:
                return self.get_input_with_input, \
                       self.activestep.prompt + "> "
            else:
                return self.get_input_with_sys_stdin, \
                       self.activestep.prompt
        else:
            return self.get_input_with_input, "Action: "

    def get_input_with_input(self, prompt):
        """
        input with the standard input
        """
        return input("{}".format(prompt))

    def get_input_with_sys_stdin(self, prompt):
        """
        input with sys.stdin.read for multiline text input
        """
        print(prompt)
        return sys.stdin.read()
