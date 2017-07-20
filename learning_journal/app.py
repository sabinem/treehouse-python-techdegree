from flask import (Flask, g, render_template, flash, redirect, url_for,
                   abort)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                             login_required, current_user)

import forms
import models
import renderer

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'auoesh.bouoastuh.43,uoausoehuosth3ououea.auoub!'

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
        return dict(user=g.owner)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user
    g.owner = models.User.get()


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


@app.route('/list')
def list_entries():
    entries = models.Entry.select()
    return render_template('entry_index.html', entries=entries)


@app.route('/resources')
def list_resources():
    resources = models.Resource.select()
    return render_template('resource_index.html', resources=resources)


@app.route('/tags')
def list_tags():
    tags = models.Tag.select()
    return render_template('tag_index.html', tags=tags)


@app.route('/entry/<int:entry_id>')
def view_entry(entry_id):
    entry = None
    try:
        entry = models.Entry.get(models.Entry.id == entry_id)
    except models.DoesNotExist:
        abort(404)
    resources = entry.get_resources()
    tags = entry.get_tags()
    return render_template('entry_detail.html', entry=entry, resources=resources, tags=tags)


@app.route('/resource/<int:resource_id>')
def view_resource(resource_id):
    resource = None
    try:
        resource = models.Resource.get(models.Resource.id == resource_id)
    except models.DoesNotExist:
        abort(404)
    return render_template('resource_detail.html', resource=resource)


@app.route('/tag/<int:tag_id>')
def view_tag(tag_id):
    tag = None
    try:
        tag = models.Tag.get(models.Tag.id == tag_id)
    except models.DoesNotExist:
        abort(404)
    entries = tag.get_entries()
    return render_template('tag_detail.html', tag=tag, entries=entries)


@app.route('/entry-add', methods=('GET', 'POST'))

def add_entry():
    form = forms.EntryForm()
    if form.validate_on_submit():
        entry = models.Entry.create(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            learned=form.learned.data,
        )
        entry.create_resources(form.resources.data)
        entry.create_tags(form.resources.data)
        flash("Entry created")
        return redirect(url_for('view_entry', entry_id=entry.id ))
    return render_template('entry_add.html', form=form)


@app.route('/resource-add', methods=('GET', 'POST'))

def add_resource():
    form = forms.ResourceForm()
    if form.validate_on_submit():
        resource = models.Resource.create(
            title=form.title.data,
            abstract=form.abstract.data,
            links=form.links.data)
        flash("Resource created")
        return redirect(url_for('view_resource', resource_id=resource.id))
    return render_template('resource_add.html', form=form)


@app.route('/tag-add', methods=('GET', 'POST'))
@login_required
def add_tag():
    form = forms.TagForm()
    if form.validate_on_submit():
        tag = models.Tag.create(
            tag=form.tag.data,
            description=form.description.data)
        flash("Tag created")
        return redirect(url_for('view_tag', tag_id=tag.id))
    return render_template('tag_add.html', form=form)


@app.route('/entry-edit/<int:entry_id>', methods=('GET', 'POST'))

def edit_entry(entry_id):
    entry = None
    try:
        entry = models.Entry.get(models.Entry.id == entry_id)
    except models.DoesNotExist:
        abort(404)
    entrywithresourcesandtags = models.EntryWithResourcesandTags(entry)
    form = forms.EntryForm(obj=entrywithresourcesandtags)
    print('????????????????????')
    print(form.tags.choices)
    if form.validate_on_submit():
        entrywithresourcesandtags.update(form)
        flash("Entry updated")
        return redirect(url_for('view_entry', entry_id=entry_id))
    return render_template('entry_edit.html', form=form)


@app.route('/resource-edit/<int:resource_id>', methods=('GET', 'POST'))

def edit_resource(resource_id):
    resource = None
    try:
        resource = models.Resource.get(models.Resource.id == resource_id)
    except models.DoesNotExist:
        abort(404)
    form = forms.ResourceForm(obj=resource)
    if form.validate_on_submit():
        form.populate_obj(resource)
        resource.save()
        flash("Resource updated")
        return redirect(url_for('list_resources'))
    return render_template('resource_edit.html', form=form)


@app.route('/tag-edit/<int:tag_id>', methods=('GET', 'POST'))
@login_required
def edit_tag(tag_id):
    tag = None
    try:
        tag = models.Tag.get(models.Tag.id == tag_id)
    except models.DoesNotExist:
        abort(404)
    form = forms.TagForm(obj=tag)
    if form.validate_on_submit():
        form.populate_obj(tag)
        tag.save()
        flash("Tag updated")
        return redirect(url_for('list_tags'))
    return render_template('tag_edit.html', form=form)


@app.route('/entry-delete/<int:entry_id>', methods=('GET', 'POST',))
@login_required
def delete_entry(entry_id):
    entry = None
    form = forms.ConfirmDeleteForm()
    try:
        entry = models.Entry.get(models.Entry.id == entry_id)
    except models.DoesNotExist:
        pass
    resources = entry.get_resources()
    tags = entry.get_tags()
    if form.validate_on_submit():
        entry.delete_resource_connections()
        entry.delete_instance()
        entry.delete_tag_connections()
        entry.delete_instance()
        flash("Entry deleted")
        return redirect(url_for('list_entries'))
    return render_template('entry_confirmdelete.html', form=form, entry=entry, resources=resources, tags=tags)


@app.route('/resource-delete/<int:resource_id>', methods=('GET', 'POST',))
@login_required
def delete_resource(resource_id):
    resource = None
    form = forms.ConfirmDeleteForm()
    try:
        resource = models.Resource.get(models.Resource.id == resource_id)
    except models.DoesNotExist:
        pass
    if form.validate_on_submit():
        resource.delete_on_entries()
        resource.delete_instance()
        flash("Resource deleted")
        return redirect(url_for('list_resources'))
    return render_template('resource_confirmdelete.html', form=form, resource=resource)


@app.route('/tag-delete/<int:tag_id>', methods=('GET', 'POST',))
@login_required
def delete_tag(tag_id):
    tag = None
    form = forms.ConfirmDeleteForm()
    try:
        tag = models.Tag.get(models.Tag.id == tag_id)
    except models.DoesNotExist:
        pass
    if form.validate_on_submit():
        tag.delete_tag_on_entries()
        tag.delete_instance()
        flash("Tag deleted")
        return redirect(url_for('list_tags'))
    return render_template('tag_confirmdelete.html', form=form, tag=tag)


@app.template_filter('mistune_markdown')
def mistune_markdown(value):
    return renderer.markdown(value)


if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)