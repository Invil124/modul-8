from mongoengine import Document
from mongoengine.fields import DateTimeField, ListField, StringField, ReferenceField


class Author(Document):
    full_name = StringField(max_length=150, unique=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField(min_length=10, unique=True)


class Quote(Document):
    tags = ListField()
    author = ReferenceField(Author)
    quote = StringField()
