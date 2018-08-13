from django.test import TestCase
from imageboard.models import Board, Thread, UserPost
from seed.factories import ThreadFactory, UserPostFactory
# Create your tests here.

class ModelTestCase(TestCase):
   
    def setUp(self):
        self.ip_addr = '127.0.0.1'
        self.board1 = Board.objects.create(name='Test board', slug='test') 
        self.thread1 = Thread.objects.create(post='Test thread!', board=self.board1, ip_address=self.ip_addr)
        self.thread2 = Thread.objects.create(post='This is a test too!', board=self.board1, ip_address=self.ip_addr)
        self.post1 = UserPost.objects.create(post='JOHNNY GUITAR', thread=self.thread1, ip_address=self.ip_addr)
        self.post2 = UserPost.objects.create(post='I hate john', name='Not john', thread=self.thread2, ip_address=self.ip_addr)
            
    def test_instances(self):
        self.assertTrue(isinstance(self.board1, Board))
        self.assertTrue(isinstance(self.thread1, Thread))
        self.assertTrue(isinstance(self.post1, UserPost))

    def test_post_numbering(self): #Test that post numbering works
        self.assertNotEqual(self.post1.post_number,self.post2.post_number)

    def test_bumbing(self): #Test that threads with more recent posts have higher bumb order
        self.assertGreater(self.thread2.bumb_order, self.thread1.bumb_order)
  
    def test_names(self): #Test that custom names work
        self.assertNotEqual(self.post1.name, self.post2.name)
    
    def test_string_method(self): #Test __str__ method
        self.assertEqual(self.board1.__str__(), self.board1.name)
        self.assertEqual(self.post1.__str__(), str(self.post1.post_number))

    def test_get_numbering(self): #Test that custom model methods work
        next_thread = Thread.get_thread_number()
        next_post = UserPost.get_post_number()
     
        self.assertEqual(next_thread, self.thread2.thread_number + 1)
        self.assertEqual(next_post, self.post2.post_number + 1)

    def test_get_date(self): #Test the custom get_date method
        self.assertEqual(self.thread1.get_date(), self.thread1.time_made.strftime("%a %H:%M, %d %b %Y"))
        self.assertEqual(self.post1.get_date(), self.post1.time_made.strftime("%a %H:%M, %d %b %Y"))

    def test_get_absolute_urls(self): #Test the get_absolute_url methods
        self.assertEqual(self.thread1.get_absolute_url(), '/board/{}/{}/'.format(self.board1.slug, self.thread1.thread_number))
        self.assertEqual(self.board1.get_absolute_url(), '/board/{}/'.format(self.board1.slug))
        self.assertEqual(self.post1.get_absolute_url(), '/board/{}/{}/'.format(self.board1.slug, self.thread1.thread_number))

    def test_create_urls(self): #Test create urls for thread an post
        self.assertEqual(self.board1.get_thread_create_url(), '/board/{}/create/'.format(self.board1.slug))
        self.assertEqual(self.thread1.get_post_create_url(), '/board/{}/{}/create/'.format(self.board1.slug, self.thread1.thread_number))
   
    def test_delete_urls(self):
        self.assertEqual(self.thread1.get_delete_url(), '/board/{}/{}/delete/'.format(self.board1.slug, self.thread1.thread_number))
        self.assertEqual(self.post1.get_delete_url(), '/board/{}/{}/{}/delete/'.format(
            self.board1.slug, self.thread1.thread_number, self.post1.post_number))

class SageTestCase(TestCase):

    def setUp(self):
        self.thread1 = ThreadFactory()
        self.thread2 = ThreadFactory()
        self.post1 = UserPostFactory(thread=self.thread1, sage=True) 

    def test_sage(self):
        self.assertGreater(self.thread2.bumb_order, self.thread1.bumb_order)

    def test_no_sage(self):
        self.post2 = UserPostFactory(thread=self.thread1)
        self.assertGreater(self.thread1.bumb_order, self.thread2.bumb_order)

class ArchivedBumpLimitTestCase(TestCase):
   
    def setUp(self):
        self.thread = ThreadFactory()
        posts = UserPostFactory.create_batch(500, thread=self.thread)
        self.thread2 = ThreadFactory()
        posts2 = UserPostFactory.create_batch(350, thread=self.thread2)
        post = UserPostFactory(thread=self.thread) #Make a post to test that bumb_order doesn't change

    def test_archiving(self):
        self.assertTrue(self.thread.archived)

    def test_bumb_limit_reached(self):
        self.assertTrue(self.thread2.bumb_limit_reached)

    def test_bumb_limit_working(self):
        self.assertGreater(self.thread2.bumb_order, self.thread.bumb_order)
