from django.test import TestCase
from imageboard.models import Board, Thread, UserPost
# Create your tests here.

class ModelTestCase(TestCase):
   
    def setUp(self):
        self.board1 = Board.objects.create(name='Test board', slug='test') 
        self.thread1 = Thread.objects.create(post='Test thread!', board=self.board1)
        self.thread2 = Thread.objects.create(post='This is a test too!', board=self.board1)
        self.post1 = UserPost.objects.create(post='JOHNNY GUITAR', thread=self.thread1)
        self.post2 = UserPost.objects.create(post='I hate john', name='Not john', thread=self.thread2)
            
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
        self.assertEqual(self.thread1.get_date(), self.thread1.time_made.strftime("%a %H:%S, %d %b %Y"))
        self.assertEqual(self.post1.get_date(), self.post1.time_made.strftime("%a %H:%S, %d %b %Y"))

    def test_get_absolute_url(self): #Test the get_absolute_url methods
        self.assertEqual(self.thread1.get_absolute_url(), '/board/{}/{}/'.format(self.board1.slug, self.thread1.thread_number)) 
