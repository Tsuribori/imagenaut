from django.test import TestCase
from django.urls import reverse
from imageboard.models import Board, Thread, UserPost

class ViewTestCase(TestCase):
    
    def setUp(self):
        self.board1 = Board.objects.create(name='Test board', slug='test') 
        self.thread1 = Thread.objects.create(post='Test thread!', board=self.board1)
        self.thread2 = Thread.objects.create(post='This is a test too!', board=self.board1)
        self.post1 = UserPost.objects.create(post='JOHNNY GUITAR', thread=self.thread1)
        self.post2 = UserPost.objects.create(post='I hate john', name='Not john', thread=self.thread2)

    def test_board_url(self): #Test the board view
        resp = self.client.get(reverse('imageboard_thread_list', kwargs={'board': self.board1.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'imageboard/board.html')
        self.assertTrue('thread_list' in resp.context)

    def test_thread_url(self): #Test the thread view
        resp = self.client.get(reverse('imageboard_thread_page', kwargs={'board': self.board1.slug, 'thread_number': self.thread1.thread_number}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'imageboard/thread.html')
        self.assertTrue('thread' in resp.context)

