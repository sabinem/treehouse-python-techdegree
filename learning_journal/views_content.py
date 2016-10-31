from flask import (render_template, flash, redirect, url_for, abort)
from flask_login import login_required
from learning_journal import renderer
from learning_journal import models
from learning_journal import forms
from learning_journal import app
from learning_journal import decorators


@app.route('/list')
@decorators.owner_required
def list_entries():
    entries = models.Entry.select()
    return render_template('entry_index.html', entries=entries)


@app.route('/resources')
@decorators.owner_required
def list_resources():
    resources = models.Resource.select()
    return render_template('resource_index.html', resources=resources)


@app.route('/tags')
@decorators.owner_required
def list_tags():
    tags = models.Tag.select()
    return render_template('tag_index.html', tags=tags)


@app.route('/entry/<int:entry_id>')
@decorators.owner_required
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
@decorators.owner_required
def view_resource(resource_id):
    resource = None
    try:
        resource = models.Resource.get(models.Resource.id == resource_id)
    except models.DoesNotExist:
        abort(404)
    entries = resource.get_entries()
    return render_template('resource_detail.html', resource=resource, entries=entries)


@app.route('/tag/<int:tag_id>')
@decorators.owner_required
def view_tag(tag_id):
    tag = None
    try:
        tag = models.Tag.get(models.Tag.id == tag_id)
    except models.DoesNotExist:
        abort(404)
    entries = tag.get_entries()
    return render_template('tag_detail.html', tag=tag, entries=entries)


@app.route('/entry-add', methods=('GET', 'POST'))
@decorators.owner_required
@login_required
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
        entry.create_tags(form.tags.data)
        flash("Entry created")
        return redirect(url_for('view_entry', entry_id=entry.id ))
    return render_template('entry_add.html', form=form)


@app.route('/resource-add', methods=('GET', 'POST'))
@decorators.owner_required
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
@decorators.owner_required
def add_tag():
    form = forms.TagForm()
    if form.validate_on_submit():
        tag = models.Tag.create(
            title=form.title.data,
            description=form.description.data)
        flash("Tag created")
        return redirect(url_for('view_tag', tag_id=tag.id))
    return render_template('tag_add.html', form=form)


@app.route('/entry-edit/<int:entry_id>', methods=('GET', 'POST'))
@login_required
@decorators.owner_required
def edit_entry(entry_id):
    entry = None
    try:
        entry = models.Entry.get(models.Entry.id == entry_id)
    except models.DoesNotExist:
        abort(404)
    entrywithresourcesandtags = models.EntryWithResourcesandTags(entry)
    form = forms.EntryForm(obj=entrywithresourcesandtags)
    if form.validate_on_submit():
        entrywithresourcesandtags.update(form)
        flash("Entry updated")
        return redirect(url_for('view_entry', entry_id=entry_id))
    return render_template('entry_edit.html', form=form)


@app.route('/resource-edit/<int:resource_id>', methods=('GET', 'POST'))
@login_required
@decorators.owner_required
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
@decorators.owner_required
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
@decorators.owner_required
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
        entry.delete_tag_connections()
        entry.delete_instance()
        flash("Entry deleted")
        return redirect(url_for('list_entries'))
    return render_template('entry_confirmdelete.html', form=form, entry=entry, resources=resources, tags=tags)


@app.route('/resource-delete/<int:resource_id>', methods=('GET', 'POST',))
@login_required
@decorators.owner_required
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
@decorators.owner_required
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