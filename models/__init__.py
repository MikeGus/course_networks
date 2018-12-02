from appconfig import psql_db
from peewee import *


def init_tables():
    psql_db.create_tables([TypeStat], safe=True)


def drop_tables():
    psql_db.drop_tables([TypeStat], safe=True)


class BaseModel(Model):
    class Meta:
        database = psql_db


class TypeStat(BaseModel):
    extension = CharField(unique=True, null=True)
    uploads = IntegerField(default=0)
    downloads = IntegerField(default=0)
