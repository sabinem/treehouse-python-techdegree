"""
This file contains basic helper-functionality
"""
import os
import sys


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def quit(**kwargs):
    """quit"""
    sys.exit()


def get_input(msg):
    return input(msg)