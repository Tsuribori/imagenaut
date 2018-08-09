from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import timedelta
from time import sleep
from imageboard.models import Board, Thread, UserPost
from imageboard.forms import ThreadForm, UserPostForm



class SetUpMixin(TestCase):
    
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

class ViewTestCase(SetUpMixin):
   

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

    
class CreateViewTestCase(TestCase):

    def setUp(self): #Must have own setUp, else CooldownMixin in imagenaut.utils will cause problems
        self.ip_addr = '127.0.0.1'
        self.board1 = Board.objects.create(name='Test board', slug='test') 
        self.thread1 = Thread.objects.create(post='Test thread!', board=self.board1, ip_address=self.ip_addr)
        self.post1 = UserPost.objects.create(post='JOHNNY GUITAR', thread=self.thread1, ip_address=self.ip_addr)
        self.old_THREAD_COOLDOWN = settings.THREAD_COOLDOWN
        settings.THREAD_COOLDOWN = 0.1
        self.old_POST_COOLDOWN = settings.POST_COOLDOWN
        settings.POST_COOLDOWN = 0.1

    def tearDown(self):
        settings.THREAD_COOLDOWN = self.old_THREAD_COOLDOWN
        settings.POST_COOLDOWN = self.old_POST_COOLDOWN        
 
    def test_thread_form(self): #Test that form page for thread displays correctly
        resp = self.client.get(reverse('imageboard_thread_create', kwargs={'board': self.board1.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)
        self.assertTrue('board' in resp.context)
        self.assertTemplateUsed(resp, 'imageboard/thread_form_page.html') 

    def test_post_form(self): #Test that form page for post displays correctly
        resp = self.client.get(reverse('imageboard_userpost_create', kwargs={'board': self.board1.slug, 'thread_number': self.thread1.thread_number}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context) 
        self.assertTrue('thread' in resp.context)
        self.assertTemplateUsed(resp, 'imageboard/userpost_form_page.html')

    def test_thread_form_post(self): #Test that threads can be made
       sleep(0.15) #Sleep so cooldown is reset and posting works
       post_made = 'This is a form test'
       resp = self.client.post(reverse('imageboard_thread_create', kwargs={'board': self.board1.slug}), {'post': post_made, 'name': 'Iodine'})
       self.assertEqual(resp.status_code, 302)
       new_thread = Thread.objects.get(post=post_made)
       self.assertEqual(new_thread.name, 'Iodine')
       self.assertEqual(new_thread.ip_address, '127.0.0.1')
 
    def test_post_form_post(self): #Test that posts can be made
       sleep(0.15)
       post_made = 'Let me give you a quick rundown'
       resp = self.client.post(reverse('imageboard_userpost_create', kwargs={'board': self.board1.slug, 'thread_number': self.thread1.thread_number}), 
           {'post': post_made, 'name': 'Bogpilled'})
       self.assertEqual(resp.status_code, 302)
       new_post = UserPost.objects.get(post=post_made)
       self.assertEqual(new_post.name, 'Bogpilled')
       self.assertEqual(new_post.ip_address, '127.0.0.1')

    def test_thread_cooldown(self):
       resp = self.client.post(reverse('imageboard_thread_create', kwargs={'board': self.board1.slug}), 
           {'post': 'Aluminium is overrated', 'name': 'Iodine'})
       self.assertEqual(resp.status_code, 200)
       self.assertFormError(resp, 'form', field='name', errors=['You must wait longer before making a new thread.'])

    def test_post_cooldown(self):
       resp = self.client.post(reverse('imageboard_userpost_create', kwargs={'board': self.board1.slug, 'thread_number': self.thread1.thread_number}), 
           {'post': 'Aluminium is overrated', 'name': 'Iodine'})
       self.assertEqual(resp.status_code, 200)
       self.assertFormError(resp, 'form', field='name', errors=['You must wait longer before making a new post.'])

       
class DeleteViewTestCase(SetUpMixin):

    def test_thread_delete_form_get(self):
        resp = self.client.get(
            reverse('imageboard_thread_delete', kwargs={
                'board': self.board1.slug, 'thread_number': self.thread1.thread_number}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'imageboard/thread_confirm_delete.html')
        self.assertTrue('thread' in resp.context)

    def test_thread_delete_form_post(self):
        resp = self.client.post(
            reverse('imageboard_thread_delete', kwargs={
                'board': self.board1.slug, 'thread_number': self.thread1.thread_number}))
        self.assertRedirects(resp, expected_url=reverse('imageboard_thread_list', kwargs={'board': self.board1.slug}), status_code=302)
        self.assertFalse(Thread.objects.filter(thread_number=self.thread1.thread_number).exists()) #Check if thread was deleted

        

    def test_userpost_delete_form_get(self):
        resp = self.client.get(
            reverse('imageboard_userpost_delete', kwargs={
                'board': self.board1.slug, 'thread_number': self.thread1.thread_number, 'post_number': self.post1.post_number}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'imageboard/userpost_confirm_delete.html')
        self.assertTrue('userpost' in resp.context)
        

    def test_userpost_delete_form_post(self):
       resp = self.client.post(
           reverse('imageboard_userpost_delete', kwargs={
               'board': self.board1.slug, 'thread_number': self.thread1.thread_number, 'post_number': self.post1.post_number}))
       self.assertRedirects(resp, expected_url=reverse('imageboard_thread_page', kwargs={
           'board': self.board1.slug, 'thread_number': self.thread1.thread_number}), status_code=302)
       self.assertFalse(UserPost.objects.filter(post_number=self.post1.post_number).exists())


