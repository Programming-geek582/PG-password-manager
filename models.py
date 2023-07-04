from tortoise.models import Model
from tortoise.fields import TextField, IntField

class User(Model):
    id = IntField(pk=True)
    firstname = TextField()
    lastname = TextField()
    username = TextField()
    token = TextField()
    password = TextField()

class Password(Model):
    id = IntField(pk=True)
    userToken = TextField()
    website = TextField()
    username = TextField()
    password = TextField()

class SharingConfig(Model):
    id = IntField(pk=True)
    sharerToken = TextField()
    viewerToken = TextField()