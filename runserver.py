"""
Just a small script to start the application
"""
from todo_api import models, config
from todo_api.app import app


if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)