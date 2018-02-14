"""
This file contains basic helper-functionality
"""
import sys


def input_wrapper(msg):
    """
    wrapper for input statements,
    so they detect the quit command to leave the application.
    """
    userinput = input(msg)
    if userinput != 'q':
        return userinput
    else:
        sys.exit()
