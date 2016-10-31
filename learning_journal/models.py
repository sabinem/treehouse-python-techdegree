"""
This file includes all the modules. It sets the database up with
peewee.
"""
import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *


DATABASE = SqliteDatabase('learningjournal.db')


class User(UserMixin, Model):
    """
    The user model includes the blog title and the name set
    for the copyright statement.
    """
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    blog_title = CharField(max_length=100)
    blog_owner = CharField(max_length=100)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(
        cls, email, password, blog_title, blog_owner, admin=False
    ):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password),
                    blog_title=blog_title,
                    blog_owner=blog_owner,
                )
        except IntegrityError:
            msg = "Something went wrong during the registartion. Try again!"
            raise ValueError(msg)


class Entry(Model):
    """
    The Entry model is the main model and includes the
    logentries: they can be tagged and they can contain
    resources.
    """
    title = CharField(max_length=100)
    date = DateField()
    time_spent = TimeField(formats='%H:%M')
    learned = TextField()

    class Meta:
        database = DATABASE

    def get_resources(self):
        """gets all resources"""
        return (Resource
                .select()
                .join(EntryToResource)
                .join(Entry)
                .where(Entry.id == self.id))

    def get_tags(self):
        """gets all tags"""
        return (Tag
                .select()
                .join(EntryToTag)
                .join(Entry)
                .where(Entry.id == self.id))

    def update_resources(self, resource_ids, resource_ids_update):
        """updates all resource connections, when an entry is saved"""
        resource_ids_delete = [
            resource_id for resource_id in resource_ids
            if resource_id not in resource_ids_update]
        resource_ids_create = [
            resource_id for resource_id in resource_ids_update
            if resource_id not in resource_ids]
        for resource_id in resource_ids_create:
            try:
                resource = Resource.get(Resource.id == resource_id)
                EntryToResource.create(
                    resource=resource,
                    entry=self
                )
            except DoesNotExist:
                pass
        for resource_id in resource_ids_delete:
            try:
                resourcetoentry = EntryToResource.get(
                    EntryToResource.resource_id == resource_id,
                    EntryToResource.entry_id == self.id
                )
                resourcetoentry.delete_instance()
            except DoesNotExist:
                pass

    def update_tags(self, tag_ids, tag_ids_update):
        """updates all tag connections, when an entry is saved"""
        tag_ids_delete = [tag_id for tag_id in tag_ids
                          if tag_id not in tag_ids_update]
        tag_ids_create = [tag_id for tag_id in tag_ids_update
                          if tag_id not in tag_ids]
        for tag_id in tag_ids_create:
            try:
                tag = Tag.get(Tag.id == tag_id)
                EntryToTag.create(
                    tag=tag,
                    entry=self
                )
            except DoesNotExist:
                pass
        for tag_id in tag_ids_delete:
            try:
                tagtoentry = EntryToTag.get(
                    EntryToTag.tag_id == tag_id,
                    EntryToTag.entry_id == self.id
                )
                tagtoentry.delete_instance()
            except DoesNotExist:
                pass

    def create_resources(self, resource_str_ids):
        """creates resource connections form tag ids"""
        for resource_str_id in resource_str_ids:
            try:
                resource = Resource.get(Resource.id == int(resource_str_id))
            except DoesNotExist:
                pass
            else:
                EntryToResource.create(
                    entry=self,
                    resource=resource
                )

    def create_tags(self, tag_str_ids):
        """creates tag connections form tag ids"""
        for tag_str_id in tag_str_ids:
            try:
                tag = Tag.get(Tag.id == int(tag_str_id))
            except DoesNotExist:
                pass
            else:
                EntryToTag.create(
                    entry=self,
                    tag=tag
                )

    def delete_resource_connections(self):
        """deletes all resource conneections for the entry"""
        resourcestoentry = \
            EntryToResource.select()\
            .where(EntryToResource.entry_id == self.id)
        for item in resourcestoentry:
            resourcetoentry = EntryToResource.get(
                EntryToResource.entry_id == item.entry_id,
                EntryToResource.resource_id == item.resource_id)
            resourcetoentry.delete_instance()

    def delete_tag_connections(self):
        """deletes all tag conneections for the entry"""
        tagstoentry = EntryToTag.select()\
            .where(EntryToTag.entry_id == self.id)
        for item in tagstoentry:
            tagtoentry = EntryToTag.get(
                EntryToTag.entry_id == item.entry_id,
                EntryToTag.tag_id == item.tag_id)
            tagtoentry.delete_instance()


class Resource(Model):
    """Resource model"""
    title = CharField(max_length=100)
    abstract = CharField(max_length=200)
    links = TextField()

    class Meta:
        database = DATABASE

    def delete_on_entries(self):
        resourcestoentries = EntryToResource.select()\
            .where(EntryToResource.resource_id == self.id)
        for resourcetoentry in resourcestoentries:
            resourcetoentry.delete_instance()

    def get_entries(self):
        return (Entry
                .select()
                .join(EntryToResource)
                .join(Resource)
                .where(Resource.id == self.id))


class Tag(Model):
    """tag model class"""
    title = CharField(max_length=30)
    description = TextField()

    class Meta:
        database = DATABASE

    def delete_tag_on_entries(self):
        """deletes all connections of a tag to entries"""
        tagstoentries = EntryToTag.select().where(EntryToTag.tag_id == self.id)
        for tagtoentry in tagstoentries:
            tagtoentry.delete_instance()

    def get_entries(self):
        """gets all entries that are tagged with the tag"""
        return (Entry
                .select()
                .join(EntryToTag)
                .join(Tag)
                .where(Tag.id == self.id))

    def get_count(self):
        """counts the tagged entries"""
        return (Entry
                .select()
                .join(EntryToTag)
                .join(Tag)
                .where(Tag.id == self.id).count())


class EntryToTag(Model):
    """A simple "through" table for many-to-many relationship entry to tag."""
    entry = ForeignKeyField(Entry)
    tag = ForeignKeyField(Tag)

    class Meta:
        database = DATABASE
        primary_key = CompositeKey('entry', 'tag')


class EntryToResource(Model):
    """A simple "through" table for many-to-many relationship entry to resource"""
    entry = ForeignKeyField(Entry)
    resource = ForeignKeyField(Resource)

    class Meta:
        database = DATABASE
        primary_key = CompositeKey('entry', 'resource')


class EntryWithResourcesandTags:
    """
    helper class that is not stored in the database
    it is used to update an entry
    along with its tags and resources
    """
    id = None
    title = None
    date = None
    time_spent = None
    learned = None
    resources = None
    tags = None

    def __init__(self, entry):
        """
        the combined record is initilized
        in the way it exists before the update
        """
        self.entry = entry
        self.id = entry.id
        self.title = entry.title
        self.date = entry.date
        self.time_spent = entry.time_spent
        self.learned = entry.learned
        _resources = self.entry.get_resources()
        _tags = self.entry.get_tags()
        self.resources = [
            (resource.id, resource.title)
            for resource in list(_resources)]
        self.tags = [(tag.id, tag.title)
                     for tag in list(_tags)]

    def update(self, form):
        """the update is performed"""
        self.entry.title = form.title.data
        self.entry.date = form.date.data
        self.entry.time_spent = form.time_spent.data
        self.entry.learned = form.learned.data
        self.entry.save()
        resource_ids_start = [tuple[0] for tuple in self.resources]
        resource_ids_form = [
            int(resource_str) for resource_str in form.resources.data]
        self.entry.update_resources(resource_ids_start, resource_ids_form)
        tag_ids_start = [tuple[0] for tuple in self.tags]
        tag_ids_form = [int(tag_str) for tag_str in form.tags.data]
        self.entry.update_tags(tag_ids_start, tag_ids_form)


def get_tag_choices():
    """
    gets the choices of tags for chosen select input field in the
    entry form
    """
    return list(Tag.select().select(Tag.id, Tag.title).tuples())


def get_resource_choices():
    """
    gets the choices of resources for chosen select input field in the
    entry form
    """
    return list(Resource.select().select(Resource.id, Resource.title).tuples())


def initialize():
    """establishes the database"""
    DATABASE.connect()
    DATABASE.create_tables([User, Entry, Resource,
                            Tag, EntryToTag, EntryToResource], safe=True)
    DATABASE.close()
