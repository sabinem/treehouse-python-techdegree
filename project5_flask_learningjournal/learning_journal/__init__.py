"""package learning_journal"""
import os

from flask import Flask

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['TEMPLATES_AUTO_RELOAD'] = True


from learning_journal import views_admin, views_content

