from django.test import TestCase
from imageboard.models import Thread, UserPost
# Create your tests here.

class ThreadTestCase(TestCase):

    def create_dummy_thread(self, subject, post):
        return Thread.objects.create(subject=subject, post=post)
    def create_test_post(self, thread):
        return UserPost.objects.create(post='This is Johnnys post', name='Johnny', thread=thread)

    def are_equal(self, one, two):
        if one == two:
            return True
        else:
            return False

    def is_bigger_than(self, bigger, smaller):
        if bigger > smaller:
            return True
        else:
            return False

    def test_models(self):
        thread1 = self.create_dummy_thread('This is a test thread','Hello World!')
        thread2 = self.create_dummy_thread('This is also a test thread!','Hello also!')
        post1 = self.create_test_post(thread1)
        post2 = self.create_test_post(thread1)

        self.assertFalse(self.are_equal(post1.post_number,post2.post_number))
        self.assertTrue(self.is_bigger_than(thread1.bumb_order, thread2.bumb_order))
        self.assertEqual(post1.name, post2.name)
        self.assertEqual(post1.__str__(), str(post1.post_number))
        self.assertFalse(self.are_equal(thread1.name,post1.name))
        self.assertTrue(isinstance(thread1, Thread))
        self.assertTrue(isinstance(post1, UserPost))
             
