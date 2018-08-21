from django.test import TestCase, tag
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import timedelta
from time import sleep
from imageboard.models import Board, Thread, UserPost
from imageboard.forms import ThreadForm, UserPostForm
from seed.factories import faker, BoardFactory, ThreadFactory, UserPostFactory



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
        resp = self.client.get(reverse('imageboard_thread_list', kwargs={'board': self.board1.slug})+'?page=3')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'imageboard/board.html')
        self.assertTrue('thread_list' in resp.context) 
        self.assertContains(resp, self.thread1.post)
        self.assertFalse(resp.context['moderation_view'])

    def test_thread_url(self): #Test the thread view
        resp = self.client.get(reverse('imageboard_thread_page', kwargs={'board': self.board1.slug, 'thread_number': self.thread1.thread_number}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'imageboard/thread.html')
        self.assertTrue('thread' and 'form' in resp.context) 
        self.assertContains(resp, self.post1.post)
        

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
        self.assertEqual(resp.context['form']['sage'].value(), False)
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

@tag('slow')
class ArchivedPostViewTestCase(TestCase):
 
    def setUp(self):
        self.thread = ThreadFactory()
        posts = UserPostFactory.create_batch(500, thread=self.thread)
    
    def test_thread_archived(self): #Test that the form is not displayed when thread archived
        resp = self.client.get(self.thread.get_absolute_url)
        self.assertTrue('form' not in resp.context)
        
    def test_thread_archived_no_posting(self): #Test that posting doesnt work when thread archived
        resp = self.client.post(self.thread.get_post_create_url(), {'post': faker.text()})
        self.assertTrue(resp.status_code, 405)

@tag('slow')
class ArchivedThreadTestCase(TestCase):

    def setUp(self):
        self.board = BoardFactory()
        self.thread = ThreadFactory(board=self.board)
        self.thread2 = ThreadFactory(board=self.board)
        threads = ThreadFactory.create_batch(110, board=self.board)
        self.thread.refresh_from_db()

    def test_thread_archived_threads(self):
        resp = self.client.get('{}?page=10'.format(self.board.get_absolute_url()))
        self.assertNotContains(resp, self.thread2.post)

    def test_no_extra_pages(self):
        resp = self.client.get('{}?page=11'.format(self.board.get_absolute_url()))
        self.assertEqual(resp.status_code, 404)

    def test_thread_archived_threads_no_posting(self):
        resp = self.client.post(self.thread.get_post_create_url(), {'post': faker.text()})
        self.assertTrue(resp.status_code, 405)
       

class ThreadReportTestCase(TestCase):

    def setUp(self):
        self.thread = ThreadFactory()
        self.get_resp = self.client.get(self.thread.get_report_url())
        self.post_resp = self.client.post(self.thread.get_report_url())
        self.thread.refresh_from_db()

    def test_template_used(self):
        self.assertTemplateUsed(self.get_resp, 'imageboard/thread_report_confirm.html')
        
    def test_context(self):
        self.assertTrue('thread' in self.get_resp.context)

    def test_context_correct(self):
        self.assertEqual(self.get_resp.context['thread'], self.thread)
        
    def test_redirect(self):
        self.assertRedirects(self.post_resp, expected_url=self.thread.get_absolute_url(), status_code=302)

    def test_thread_reported(self):
        self.assertTrue(self.thread.reported)

class UserPostReportTestCase(TestCase):

    def setUp(self):
        self.post = UserPostFactory()
        self.get_resp = self.client.get(self.post.get_report_url())
        self.post_resp = self.client.post(self.post.get_report_url())
        self.post.refresh_from_db()

    def test_template_used(self):
        self.assertTemplateUsed(self.get_resp, 'imageboard/userpost_report_confirm.html')
        
    def test_context(self):
        self.assertTrue('userpost' in self.get_resp.context)

    def test_context_correct(self):
        self.assertEqual(self.get_resp.context['userpost'], self.post)
        
    def test_redirect(self):
        self.assertRedirects(self.post_resp, expected_url=self.post.get_absolute_url(), status_code=302)

    def test_thread_reported(self):
        self.assertTrue(self.post.reported)

