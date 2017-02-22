from connectdatabase import ConnectDatabase
from peewee import *


class User_stories(Model):
    title = CharField()
    text = CharField()
    criteria = CharField()
    business_value = IntegerField()
    estimation = FloatField()
    status = CharField()

    class Meta:
        database = ConnectDatabase.psql_db
