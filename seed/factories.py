import factory
import pytz
from faker import Factory

from imageboard.models import Board, Thread, UserPost
from moderation.models import Transgression

faker = Factory.create()

class BoardFactory(factory.DjangoModelFactory):
    class Meta:
        model = Board
    
    name = factory.LazyAttribute(lambda _: faker.name()) #These need to be unique
    slug = factory.LazyAttribute(lambda _: faker.slug())

class ThreadFactory(factory.DjangoModelFactory):
    class Meta:
        model = Thread

    subject = faker.word()
    name = faker.name()
    post = factory.LazyAttribute(lambda _: faker.text())
    board = factory.SubFactory(BoardFactory)
    ip_address = faker.ipv4()
    

class UserPostFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserPost

    name = faker.name()
    post = factory.LazyAttribute(lambda _: faker.text())
    thread = factory.SubFactory(ThreadFactory)
    ip_address = faker.ipv4()

class TransgressionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Transgression
   
    ip_address =  faker.ipv4()
    banned_until = faker.future_date(tzinfo=pytz.utc)
    reason = faker.text(max_nb_chars=150) #Need to set max character limit, as default for faker is max_nb_chars=200, which is over the model defined limit
