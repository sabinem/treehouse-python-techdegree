"""
Tests for the Base Dialog
"""
import sys
import unittest
from unittest.mock import patch
patch.object = patch.object

from worklogdb.worklog.base_dialog import BaseDialog, ChoiceList, DialogStep


class TestBaseDialogSetUp(unittest.TestCase):
    """
    the setup of the dialog is tested
    """
    def setUp(self):
        """
        the dialog is started
        """
        self.dialog = BaseDialog()

    def test_base_init(self):
        """
        dialogsteps and msg should be initiated
        """
        self.assertIsNone(self.dialog.choice_list)
        self.assertIsNone(self.dialog.choice)
        self.assertIsNone(self.dialog.active_choice_index)
        self.assertIsNone(self.dialog.active_choice_item)
        self.assertIsNone(self.dialog.msg)

    def test_base_get_menu(self):
        """
        the menu should know the two option 'b' for back and 'q' for quit
        """
        menu = self.dialog.get_menu()
        self.assertIn('b', menu)
        self.assertIn('q', menu)

    def test_base_get_first_dialogsteps(self):
        """
        there should be a function to get the dialogsteps and the
        dialogsteps should be empty for the base dialog
        """
        self.assertIsNone(self.dialog.get_first_dialogstep())

    def test_base_back(self):
        """
        there should be a function to go back to the previous dialog and
        it should return nothing
        """
        self.dialog.back()
        self.assertTrue(self.dialog.quit_dialog)

    def test_base_check_for_dialog_goal(self):
        """
        checks wether the dialogs goal is reached: this method will be overwritten
        by the dialogs
        """
        self.dialog.check_for_dialog_goal()


class TestBaseDialogReturn(unittest.TestCase):
    """
    checks the dialogs return
    """
    def setUp(self):
        """
        the dialog is started and some return message is set
        """
        self.dialog = BaseDialog()
        self.dialog.return_msg = "some message"

    def test_base_get_return_parameters(self):
        """
        the method returns the returns the return message
        """
        msg = self.dialog.get_return_parameters()
        self.assertEqual(msg, "some message")


class TestBaseDialogInLoop(unittest.TestCase):
    """
    tests functionality that is called in the loop of the method main
    """
    def setUp(self):
        """
        the dialog is setup with a menu
        """
        self.dialog = BaseDialog()
        self.dialog.menu = self.dialog.get_menu()

    def test_base_update_menu(self):
        """
        the menu should know the two option 'b' for back and 'q' for quit
        """
        self.assertEqual(self.dialog.menu, self.dialog.update_menu())

    def test_base_get_method_and_prompt_choice_true(self):
        """
        choice has priority over active step: input method is input
        """
        self.dialog.choice = True
        self.dialog.activestep = DialogStep()
        method, prompt = self.dialog.get_method_and_prompt()
        self.assertEqual(method, self.dialog.get_input_with_input)
        self.assertIsNotNone(prompt)

    def test_base_get_method_and_prompt_no_choice_no_active_step_get_default(self):
        """
        if choice is false active step determines the input method
        """
        self.dialog.choice = False
        self.dialog.activestep = None
        method, prompt = self.dialog.get_method_and_prompt()
        self.assertEqual(method, self.dialog.get_input_with_input)
        self.assertIsNotNone(prompt)

    def test_base_get_method_and_prompt_no_choice_active_step_normal_input(self):
        """
        if choice is false active step determines the input method
        """
        self.dialog.choice = False
        self.dialog.activestep = DialogStep(input_method=input)
        method, prompt = self.dialog.get_method_and_prompt()
        self.assertEqual(method, self.dialog.get_input_with_input)
        self.assertIsNotNone(prompt)

    def test_base_get_method_and_prompt_no_choice_active_step_sys_input(self):
        """
        if choice is false active step determines the input method
        """
        self.dialog.choice = False
        self.dialog.activestep = DialogStep(input_method=sys.stdin.read)
        method, prompt = self.dialog.get_method_and_prompt()
        self.assertEqual(method, self.dialog.get_input_with_sys_stdin)
        self.assertIsNotNone(prompt)

    @patch.object(BaseDialog, 'get_first_dialogstep')
    @patch.object(BaseDialog, 'get_menu')
    def test_base_init_main(self, mock_get_menu, mock_get_step):
        """
        the main dialog is initialized with a menu and an active
        dialogstep
        """
        mock_get_menu.return_value = "menu"
        mock_get_step.return_value = "step"
        self.dialog.init_main()
        self.assertEqual(self.dialog.menu, "menu")
        self.assertEqual(self.dialog.activestep, "step")

    @patch.object(BaseDialog, 'print_data')
    @patch.object(BaseDialog, 'update_menu')
    def test_base_print_screen(self, mock_menu, mock_print):
        """
        the menu is update and the screen is printed
        """
        self.dialog.print_screen()
        mock_menu.assert_called_once_with()
        mock_print.assert_called_once_with()


class TestBaseDialogWithChoiceList(unittest.TestCase):
    """
    the list choice functionlity is tested
    """
    def setUp(self):
        """
        the dialog is setup with a list
        """
        self.dialog = BaseDialog()
        self.dialog.menu = self.dialog.get_menu()
        self.dialog.choice_list = ChoiceList(list=['a', 'b', 'c'])
        self.dialog.choice = True

    def test_base_print_data_with_choice(self):
        """
        the list should be included in the print stack
        """
        print_stack = self.dialog.build_print_data()
        self.assertIn("[1] a", print_stack)
        self.assertIn("[2] b", print_stack)
        self.assertIn("[3] c", print_stack)

    def test_base_check_valid_choice_list_index_valid_row_nr(self):
        """
        a chosen row number should deliver the right value
        """
        testvalue = self.dialog.check_valid_choice_list_index('1')
        self.assertTrue(testvalue)
        self.assertEqual(self.dialog.active_choice_index, 0)
        self.assertFalse(self.dialog.choice)

    def test_base_check_valid_choice_list_index_unvalid_row_nr(self):
        """
        for an unvalid row number, the user should receive a message
        """
        testvalue = self.dialog.check_valid_choice_list_index('4')
        self.assertIsNone(testvalue)
        self.assertIsNotNone(self.dialog.msg)
        self.assertIsNone(self.dialog.active_choice_index)
        self.assertTrue(self.dialog.choice)

    def test_base_check_valid_choice_list_index_unvalid_input(self):
        """
        for an unvalid input the user receives a message
        """
        testvalue = self.dialog.check_valid_choice_list_index('a')
        self.assertIsNone(testvalue)
        self.assertIsNotNone(self.dialog.msg)
        self.assertIsNone(self.dialog.active_choice_index)
        self.assertTrue(self.dialog.choice)


class TestBaseDialogWithChoiceDetail(unittest.TestCase):
    """
    tests the case of a choice detail
    """
    def setUp(self):
        """
        a choice list is set up and a choice has been made
        :return:
        """
        self.dialog = BaseDialog()
        self.dialog.menu = self.dialog.get_menu()
        self.dialog.choice_list = ChoiceList(list=['a', 'b', 'c'])
        self.dialog.choice = False
        self.dialog.active_choice_index = 0
        self.dialog.active_choice_item = 'a'

    def test_base_print_data_with_active_choice_item_and_active_index(self):
        """
        the data of the choice shoud be included in the print stack,
        but the list data should not
        """
        print_stack = self.dialog.build_print_data()
        self.assertIn("[1] a", print_stack)
        self.assertNotIn("[2] b", print_stack)
        self.assertNotIn("[3] c", print_stack)


class TestBaseDialogInLoopNoStepNoChoice(unittest.TestCase):
    """
    tests the processing of the userinput, that is called
    in the main loop
    """
    def setUp(self):
        """
        the dialog is setup with a menu, choice is false and
        there is no dialogstep set.
        """
        self.dialog = BaseDialog()
        self.dialog.menu = self.dialog.get_menu()
        self.dialog.activestep = None
        self.dialog.choice = False
        self.dialog.menu['a'] = self.dialog.update_menu

    def test_base_process_userinput_not_a_menu_choice(self):
        """
        if the choice is not in the menu the user receives a
        message
        """
        self.dialog.process_userinput("x")
        self.assertIsNotNone(self.dialog.msg)

    @patch.object(BaseDialog, 'get_menu')
    @patch.object(BaseDialog, 'check_valid_choice_list_index')
    def test_base_menu_has_priority(self, choice_mock, menu_mock):
        """
        choice but no active step: choice is tested and then the choice
        function is called
        get_menu serves here as choice function, just for the test
        """
        self.dialog.choice = True
        self.dialog.choice_list = ChoiceList(list=['a', 'b', 'c'],
                                             choice_func=self.dialog.get_menu)
        choice_mock.return_value = True
        self.dialog.process_userinput("2")
        choice_mock.assert_called_once_with("2")
        menu_mock.assert_called_once_with()

    @patch.object(BaseDialog, 'get_menu')
    @patch.object(BaseDialog, 'check_valid_choice_list_index')
    def test_base_menu_has_priority(self, choice_check_mock, choice_process_mock):
        """
        choice but no active step: choice is tested and if it fails the choice
        function is not called
        """
        self.dialog.choice = True
        self.dialog.choice_list = ChoiceList(list=['a', 'b', 'c'],
                                             choice_func=self.dialog.get_menu)
        choice_check_mock.return_value = False
        self.dialog.process_userinput("4")
        choice_check_mock.assert_called_once_with("4")
        self.assertFalse(choice_process_mock.called)



"""
    userinput = userinput.strip()
    menuchoice = userinput.lower()

    if menuchoice in self.menu:
        self.menu[menuchoice]()
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
                return self.msg"""



