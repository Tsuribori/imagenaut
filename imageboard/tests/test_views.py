from django.test import TestCase
from django.urls import reverse
from imageboard.models import Board, Thread, UserPost
from imageboard.forms import ThreadForm, UserPostForm

class ViewTestCase(TestCase):
    
    def setUp(self):
        self.ip_addr = '127.0.0.1'
        self.board1 = Board.objects.create(name='Test board', slug='test') 
        self.thread1 = Thread.objects.create(post='Test thread!', board=self.board1, ip_address=self.ip_addr)
        self.thread2 = Thread.objects.create(post='This is a test too!', board=self.board1, ip_address=self.ip_addr)
        self.post1 = UserPost.objects.create(post='JOHNNY GUITAR', thread=self.thread1, ip_address=self.ip_addr)
        self.post2 = UserPost.objects.create(post='I hate john', name='Not john', thread=self.thread2, ip_address=self.ip_addr)
        number_of_threads = 21
        for number in range(number_of_threads): #Create 21 thread to test pagination
            Thread.objects.create(post=str(number), board=self.board1, ip_address=self.ip_addr)


    def test_board_url(self): #Test the board view
        resp = self.client.get(reverse('imageboard_thread_list', kwargs={'board': self.board1.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'imageboard/board.html')
        self.assertTrue('thread_list' in resp.context)

    def test_thread_url(self): #Test the thread view
        resp = self.client.get(reverse('imageboard_thread_page', kwargs={'board': self.board1.slug, 'thread_number': self.thread1.thread_number}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'imageboard/thread.html')
        self.assertTrue('thread' and 'form' in resp.context)
        

    def test_pagination(self): #Test that pagination works
        resp = self.client.get(reverse('imageboard_thread_list', kwargs={'board': self.board1.slug}))
        self.assertTrue('is_paginated' and 'form' and 'board' in resp.context)
        self.assertTrue(len(resp.context['thread_list']) == 10)
        
    def test_pagination_url(self): #Test that page url is in form '?page=' and that last page contains right amount of threads
        resp = self.client.get(reverse('imageboard_thread_list', kwargs={'board': self.board1.slug}) + '?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' and 'form' and 'board' in resp.context)
        self.assertTrue(len(resp.context['thread_list']) == 3)

    #Form view tests below
   
    def test_thread_form(self): #Test that form page for thread displays correctly
        resp = self.client.get(reverse('imageboard_thread_create', kwargs={'board': self.board1.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)
        self.assertTemplateUsed(resp, 'imageboard/userpost_form_page.html') 

    def test_post_form(self): #Test that form page for post displays correctly
        resp = self.client.get(reverse('imageboard_userpost_create', kwargs={'board': self.board1.slug, 'thread_number': self.thread1.thread_number}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)
        self.assertTemplateUsed(resp, 'imageboard/userpost_form_page.html')

    def test_thread_form_post(self): #Test that threads can be made
       post_made = 'This is a form test'
       resp = self.client.post(reverse('imageboard_thread_create', kwargs={'board': self.board1.slug}), {'post': post_made, 'name': 'Iodine'})
       self.assertEqual(resp.status_code, 302)
       new_thread = Thread.objects.get(post=post_made)
       self.assertEqual(new_thread.name, 'Iodine')
       self.assertEqual(new_thread.ip_address, '127.0.0.1')
 
    def test_post_form_post(self): #Test that posts can be made
       post_made = 'Let me give you a quick rundown'
       resp = self.client.post(reverse('imageboard_userpost_create', kwargs={'board': self.board1.slug, 'thread_number': self.thread1.thread_number}), 
           {'post': post_made, 'name': 'Bogpilled'})
       self.assertEqual(resp.status_code, 302)
       new_post = UserPost.objects.get(post=post_made)
       self.assertEqual(new_post.name, 'Bogpilled')
       self.assertEqual(new_post.ip_address, '127.0.0.1')
       
