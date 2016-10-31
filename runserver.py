from learning_journal import models, app


if __name__ == "__main__":
    models.initialize()
    app.run(debug=True)