from flask import Flask

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'auoesh.bouoastuh.43,uoausoehuosth3ououea.auoub!'
app.config['TEMPLATES_AUTO_RELOAD'] = True

from learning_journal import views_admin, views_content

