from datetime import datetime

import peewee

from db_utilities.database_manager import DatabaseManager
from settings import DATABASE

database_manager = DatabaseManager(
    database_name=DATABASE['NAME'],
    user=DATABASE['USER'],
    password=DATABASE['PASSWORD'],
    host=DATABASE['HOST'],
    port=DATABASE['PORT'],
)


class BaseModel(peewee.Model):
    created_at = peewee.DateTimeField(default=datetime.now(), verbose_name='Created At')
    # If its necessary
    updated_at = peewee.DateTimeField(default=datetime.now(), verbose_name='Updated At')

    class Meta:
        database = database_manager.db

    # def save(self, update=True, *args, **kwargs):
    #     if not self.id:
    #         self.created_at = datetime.now()
    #     else:
    #         if update:
    #             self.updated_at = datetime.now()
    #         else:
    #             return None
    #     return super().save(*args, **kwargs)


class Category(BaseModel):
    name = peewee.CharField(max_length=255, null=False, verbose_name='Title')


class Author(BaseModel):
    name = peewee.CharField(max_length=255, null=False, verbose_name='Name')


class Post(BaseModel):
    id = peewee.IntegerField(primary_key=True, null=False, verbose_name='Id')
    title = peewee.CharField(max_length=255, null=False, verbose_name='Name')
    link = peewee.CharField(max_length=255, null=False, verbose_name='Link')
    category = peewee.ForeignKeyField(model=Category, null=False, verbose_name='Category')
    author = peewee.ForeignKeyField(model=Author, null=False, verbose_name='Author')


class Tag(BaseModel):
    id = peewee.IntegerField(primary_key=True, null=False, verbose_name='id')
    name = peewee.CharField(max_length=255, null=False, verbose_name='Title')


class PostTags(BaseModel):
    tag = peewee.ForeignKeyField(model=Tag, null=False, verbose_name='Tag')
    post = peewee.ForeignKeyField(model=Post, null=False, verbose_name='Post')


class Keyword(BaseModel):
    name = peewee.CharField(max_length=255, null=False, unique=True, verbose_name='Name')


class KeywordResult(BaseModel):
    keyword = peewee.ForeignKeyField(model=Keyword, null=False, verbose_name='Keyword')


class KeywordResultItem(BaseModel):
    KeywordResult = peewee.ForeignKeyField(model=KeywordResult, null=False, verbose_name='Keyword Result')
    post = peewee.ForeignKeyField(model=Post, null=False, verbose_name='Post')
