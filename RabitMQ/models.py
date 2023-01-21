from mongoengine import Document
from mongoengine.fields import DateTimeField, StringField, BooleanField


class Contact(Document):
    full_name = StringField(min_length=3)
    email = StringField(min_length=5, unique=True)
    date_of_registration = DateTimeField()
    send_message = BooleanField()
