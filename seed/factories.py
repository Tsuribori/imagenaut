import factory
import pytz
import os
import sys
from random import randrange
from datetime import timedelta
from faker import Factory
from django.contrib.auth.models import User, Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.utils import timezone
from imageboard.models import Board, Thread, UserPost
from moderation.models import Transgression
from rules.models import Rule

faker = Factory.create()

class BoardFactory(factory.DjangoModelFactory):
    class Meta:
        model = Board
    
    name = factory.LazyAttribute(lambda _: faker.name()) #These need to be unique
    slug = factory.LazyAttribute(lambda _: faker.slug())

class ThreadFactory(factory.DjangoModelFactory):
    class Meta:
        model = Thread
        exclude = ('files',)

    subject = faker.word()
    name = faker.name()
    post = factory.LazyAttribute(lambda _: faker.text())
    board = factory.SubFactory(BoardFactory)
    ip_address = faker.ipv4()
    image = factory.django.ImageField()
    

class UserPostFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserPost

    name = faker.name()
    post = factory.LazyAttribute(lambda _: faker.text())
    thread = factory.SubFactory(ThreadFactory)
    ip_address = faker.ipv4()
    image = factory.django.ImageField()

class TransgressionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Transgression
   
    ip_address =  faker.ipv4()
    banned_until = faker.future_date(tzinfo=pytz.utc)
    reason = faker.text(max_nb_chars=150) #Need to set max character limit, as default for faker is max_nb_chars=200, which is over the model defined limit
    banned_from = factory.SubFactory(BoardFactory)

class RuleFactory(factory.DjangoModelFactory):
    class Meta:
        model = Rule

    text = faker.text()
    board = factory.SubFactory(BoardFactory)

class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.LazyAttribute(lambda _: faker.word())
 
class ModeratorFactory():
    def create_mod():
        user = UserFactory()
        perm1 = Permission.objects.get(name='Can delete thread')
        perm2 = Permission.objects.get(name='Can delete user post')
        perm3 = Permission.objects.get(name='Can add transgression')
        permission_list = [perm1, perm2, perm3]
        for permission in permission_list:
            user.user_permissions.add(permission)
        user.refresh_from_db()
        return user

class ImageFactory():
    def __new__(cls):
        img = open(os.path.join(settings.BASE_DIR, 'seed/example_picture.jpg'), 'rb')
        return SimpleUploadedFile(img.name, img.read())

class DateFactory():
    def last_year():
        return timezone.now() - timedelta(days=365.3)

    def last_month():
        now = timezone.now()
        if now.day < 15:
            return now - timedelta(days=15)
        else:
           return now - timedelta(days=31)

    def yesterday():
        return timezone.now() - timedelta(days=1)

    def month():
        return randrange(1, 13)
    
    def day_of_month():
        return randrange(1, 33)
