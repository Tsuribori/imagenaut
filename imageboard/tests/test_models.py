from django.test import TestCase
from imageboard.models import Thread, UserPost
# Create your tests here.

class ModelTestCase(TestCase):
   
    def setUp(self):
 
        self.thread1 = Thread.objects.create(post='Test thread!')
        self.thread2 = Thread.objects.create(post='This is a test too!')
        self.post1 = UserPost.objects.create(post='JOHNNY GUITAR', thread=self.thread1)
        self.post2 = UserPost.objects.create(post='I hate john', name='Not john', thread=self.thread2)
            
    def test_instances(self):
        self.assertTrue(isinstance(self.thread1, Thread))
        self.assertTrue(isinstance(self.post1, UserPost))

    def test_post_numbering(self): #Test that post numbering works
        self.assertNotEqual(self.post1.post_number,self.post2.post_number)

    def test_bumbing(self): #Test that threads with more recent posts have higher bumb order
        self.assertGreater(self.thread2.bumb_order, self.thread1.bumb_order)
  
    def test_names(self): #Test that custom names work
        self.assertNotEqual(self.post1.name, self.post2.name)
    
    def test_string_method(self): #Test __str__ method for post
        self.assertEqual(self.post1.__str__(), str(self.post1.post_number))

    def test_get_numbering(self): #Test that custom model methods work
        next_thread = Thread.get_thread_number()
        next_post = UserPost.get_post_number()
     
        self.assertEqual(next_thread, self.thread2.thread_number + 1)
        self.assertEqual(next_post, self.post2.post_number + 1)

