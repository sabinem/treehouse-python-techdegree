"""
models for the todoapi:
- user
- todos
"""
import datetime

# for password hashing
import argon2
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
# peewee is used as ORM for SQLlite
from peewee import *

from . import config

DATABASE = SqliteDatabase('todos.sqlite')

# a password hasher is used
HASHER = argon2.PasswordHasher()

testuser_data = {
    'username': 'testuser',
    'email': 'test@gmail.com',
    'password': 'treehouse',
    'verify_password': 'treehouse'
}


class User(Model):
    """User model"""
    email = CharField(unique=True)
    username = CharField(unique=True)
    password = CharField()
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        """it is checked whether the
        given email or password exists already:
        if not the new user is created

        this is necessary since peewee does not
        include validation!
        """
        try:
            cls.select().where(
                (cls.email==email)|(cls.username**username)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = user.set_password(password)
            user.save()
            return user
        else:
            raise Exception("User with that email or username already exists")

    @staticmethod
    def verify_auth_token(token):
        """verifying the token"""
        serializer = Serializer(config.SECRET_KEY)
        try:
            data = serializer.loads(token)
        except (SignatureExpired, BadSignature):
            return None
        else:
            user = User.get(User.id==data['id'])
            return user

    @staticmethod
    def set_password(password):
        """hashing the password
        when a new user is created"""
        return HASHER.hash(password)

    def verify_password(self, password):
        """verifying the password hash
        when a user logs in"""
        try:
            HASHER.verify(self.password, password)
        except (argon2.exceptions.VerifyMismatchError):
            return False
        else:
            return True

    def generate_auth_token(self, expires=3600):
        """generating a token:
        this is created from the secret key"""
        serializer = Serializer(config.SECRET_KEY, expires_in=expires)
        return serializer.dumps({'id': self.id})


class Todo(Model):
    """Todos"""
    name = CharField()
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DATABASE


def initialize():
    """the database is setup, creating a new one
    at the start of the project"""
    DATABASE.connect()
    DATABASE.create_tables([User, Todo], safe=True)
    if User.select().count() == 0:
        User.create_user(**testuser_data)
    DATABASE.close()