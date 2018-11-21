from django.test import TestCase, tag
from django.core.signing import Signer
from imageboard.models import Board, Thread, UserPost
from seed.factories import faker, BoardFactory, ThreadFactory, UserPostFactory
# Create your tests here.

@tag('current')
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
 
    def test_ban_urls(self):
        self.assertEqual(self.thread1.get_ban_url(), '/mod/thread/{}/ban/'.format(self.thread1.thread_number))
        self.assertEqual(self.post1.get_ban_url(), '/mod/post/{}/ban/'.format(self.post1.post_number))

    def test_report_urls(self):
        self.assertEqual(self.thread1.get_report_url(), '/board/{}/{}/report/'.format(self.board1.slug, self.thread1.thread_number))
        self.assertEqual(self.post1.get_report_url(), '/board/{}/{}/{}/report/'.format(
            self.board1.slug, self.thread1.thread_number, self.post1.post_number))

    def test_report_dismiss_urls(self):
        self.assertEqual(self.thread1.get_report_dismiss_url(), '/mod/reports/dismiss/thread/{}/'.format(self.thread1.thread_number))
        self.assertEqual(self.post1.get_report_dismiss_url(), '/mod/reports/dismiss/post/{}/'.format(self.post1.post_number))

    def test_catalog_url(self):
        self.assertEqual(self.board1.get_catalog_url(), '/board/{}/catalog/'.format(self.board1.slug))

    def test_reported_threads_url(self):
        self.assertEqual(self.board1.get_reported_threads_url(), '/mod/reports/threads/?board={}'.format(self.board1.slug))

    def test_reported_posts_url(self):
        self.assertEqual(self.board1.get_reported_posts_url(), '/mod/reports/posts/?board={}'.format(self.board1.slug))

    def test_archive_url(self):
        self.assertEqual(self.thread1.get_archive_url(), '/archive/{}/'.format(self.board1.slug))

    def test_archive_year_url(self):
        self.assertEqual(self.thread1.get_archive_year_url(), '/archive/{}/{}/'.format(self.board1.slug, self.thread1.time_made.year))

    def test_archive_month_url(self):
        self.assertEqual(self.thread1.get_archive_month_url(), '/archive/{}/{}/{}/'.format(
            self.board1.slug, self.thread1.time_made.year, self.thread1.time_made.month))
     
    def test_archive_day_url(self):
        self.assertEqual(self.thread1.get_archive_day_url(), '/archive/{}/{}/{}/{}/'.format(
            self.board1.slug, self.thread1.time_made.year, self.thread1.time_made.month, self.thread1.time_made.day))

    
    def test_thread_number_editable(self):
        field = Thread._meta.get_field('thread_number')
        self.assertFalse(field.editable)

    def test_thread_thread_time_made_editable(self):
        field = Thread._meta.get_field('time_made')
        self.assertFalse(field.editable)

    def test_thread_poster_id_editable(self):
        field = Thread._meta.get_field('poster_id')
        self.assertFalse(field.editable)
  
    def test_post_number_editable(self):
        field = UserPost._meta.get_field('post_number')
        self.assertFalse(field.editable)

    def test_post_time_made_editable(self):
        field = UserPost._meta.get_field('time_made')
        self.assertFalse(field.editable)

    def test_post_poster_id_editable(self):
        field = UserPost._meta.get_field('poster_id')
        self.assertFalse(field.editable) 


class SageTestCase(TestCase):

    def setUp(self):
        self.thread1 = ThreadFactory()
        self.thread2 = ThreadFactory()
        self.post1 = UserPostFactory(thread=self.thread1, sage=True)
        self.thread1.refresh_from_db() 

    def test_sage(self):
        self.assertGreater(self.thread2.bumb_order, self.thread1.bumb_order)

    def test_no_sage(self):
        self.post2 = UserPostFactory(thread=self.thread1)
        self.assertGreater(self.thread1.bumb_order, self.thread2.bumb_order)

@tag('slow')
class ArchivedBumpLimit(TestCase):
   
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

@tag('slow')
class ArchivalOnThreadLimit(TestCase): #Test that old threads are "bumbed off" when a new thread is made
 
    def setUp(self):
        self.board = BoardFactory()
        self.old_thread = ThreadFactory(board=self.board)
        threads = ThreadFactory.create_batch(100, board=self.board) #Make enough new threads to archive the old
        self.old_thread.refresh_from_db() #Get the refreshed data 


    def test_bumping_off(self): 
        self.assertTrue(self.old_thread.archived)


class Pinned(TestCase):

    def setUp(self):
        self.thread = ThreadFactory(pinned=True)
        self.posts = UserPostFactory.create_batch(500, thread=self.thread)
        self.thread.refresh_from_db()

    def test_no_archiving_when_pinned(self): #Test that thread isn't archived when it is pinned
        self.assertFalse(self.thread.archived)

class PinnedOrdering(TestCase): #Test that pinned threads are always displayed first

    def setUp(self):
        self.board = BoardFactory()
        self.pinned_thread = ThreadFactory(pinned=True, board=self.board)
        self.regular_thread = ThreadFactory(board=self.board)

    def test_ordering(self):
        threads = Thread.objects.all()
        self.assertEqual(threads[0], self.pinned_thread)


class PosterID(TestCase):

    def setUp(self):
        self.thread = ThreadFactory(id_enabled=True)
        self.post = UserPostFactory(thread=self.thread)
        value1 = str(self.post.ip_address) + str(self.thread.thread_number)
        value2 = str(self.thread.ip_address) + str(self.thread.thread_number)
        signer = Signer() 
        self.unique_post_id = signer.sign(value1)[-10:]
        self.unique_thread_id = signer.sign(value2)[-10:]


    def test_id_enabled(self):
        self.assertTrue(self.thread.id_enabled)

    def test_thread_id_exists(self):
        self.assertTrue(self.thread.poster_id)

    def test_poster_id_exists(self):
        self.assertTrue(self.post.poster_id)

    def test_thread_is_length(self):
        self.assertEqual(len(self.thread.poster_id), 10)

    def test_post_id_length(self):
        self.assertEqual(len(self.post.poster_id), 10)

    def test_thread_hashes_match(self):
        self.assertEqual(self.thread.poster_id, self.unique_thread_id)

    def test_post_hashes_match(self):
        self.assertEqual(self.post.poster_id, self.unique_post_id)


class MakeTripcodeTestCase(TestCase): #Test tripcode processing

    def setUp(self):
        name = 'Name #test' 
        post = UserPostFactory(name=name)
        signer = Signer()
        tripcode = '!{}'.format(signer.sign('#test')[-10:]) #Process the expected tripcode
        self.processed_name = name.replace('#test', tripcode)
        self.trip_name = post.name
        #Below set up a test for a name without a trip to check that there are no unintended processing or errors
        self.name_without_trip = 'Name'
        post2 = UserPostFactory(name=self.name_without_trip)
        self.no_trip = post2.name

    def test_names_equal(self): #Test that the outcome is what is expected
        self.assertEqual(self.trip_name, self.processed_name)

    def test_trip_not_processed(self):
        self.assertEqual(self.name_without_trip, self.no_trip)
