from flask import (g, render_template, flash, redirect, url_for)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                             login_required, current_user)

from learning_journal import models
from learning_journal import forms
from learning_journal import app

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.context_processor
def inject_owner():
    try:
        return dict(owner=g.owner)
    except AttributeError:
        return dict(owner=None)


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    try:
        g.user = current_user
        g.owner = models.User.get()
    except models.DoesNotExist:
        pass


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/register', methods=('GET', 'POST'))
@app.route('/', methods=('GET', 'POST'))
def register():
    try:
        models.User.select().get()
    except models.DoesNotExist:
        pass
    else:
        return redirect(url_for('list_entries'))
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        models.User.create_user(
            email=form.email.data,
            password=form.password.data,
            blog_owner = form.blog_owner.data,
            blog_title = form.blog_title.data,
        )
        return redirect(url_for('list_entries'))
    return render_template('register.html', form=form, start=True)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('list_entries'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('list_entries'))
