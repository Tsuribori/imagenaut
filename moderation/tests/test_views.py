from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from imagenaut.settings import LOGIN_REDIRECT_URL
from imageboard.models import Board, Thread, UserPost
from moderation.models import Transgression

class BanViewTestCase(TestCase):
    
    def setUp(self):
        self.ip_addr = '127.0.0.1' 
        self.board1 = Board.objects.create(name='Test board', slug='test')
        self.thread1 = Thread.objects.create(post='Test thread!', board=self.board1, ip_address=self.ip_addr)
        self.post1 = UserPost.objects.create(post='JOHNNY GUITAR', thread=self.thread1, ip_address=self.ip_addr)
        self.ban1 = Transgression.objects.create(banned_until=timezone.now()+timedelta(weeks=9001), reason='Not liking the mods!', ip_address=self.ip_addr)
        self.ban_data = {'banned_until':'2049-07-22', 'reason':'Breaking the rules.'}        
    
    def test_thread_ban_get(self):
        resp = self.client.get(reverse('dj-mod:moderation_thread_ban', kwargs={'thread_number':self.thread1.thread_number}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'moderation/transgression_form.html')
        self.assertTrue('form' in resp.context)
        
    def test_thread_ban_post(self):
        resp = self.client.post(reverse('dj-mod:moderation_thread_ban', kwargs={'thread_number':self.thread1.thread_number}), self.ban_data)
        self.assertEqual(resp.status_code, 302)
        new_ban = Transgression.objects.get(reason=self.ban_data['reason'])
        self.assertEqual(new_ban.reason, self.ban_data['reason']) 
        self.assertEqual(new_ban.ip_address, '127.0.0.1')

    def test_userpost_ban_get(self):
        resp = self.client.get(reverse('dj-mod:moderation_userpost_ban', kwargs={'post_number':self.post1.post_number}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'moderation/transgression_form.html')
        self.assertTrue('form' in resp.context)

    def test_userpost_ban_post(self):
        resp = self.client.post(reverse('dj-mod:moderation_userpost_ban', kwargs={'post_number':self.post1.post_number}), self.ban_data)
        self.assertEqual(resp.status_code, 302)
        new_ban = Transgression.objects.get(reason=self.ban_data['reason'])
        self.assertEqual(new_ban.reason, self.ban_data['reason']) 
        self.assertEqual(new_ban.ip_address, '127.0.0.1')

 
    def test_ban_page_redirect(self): #Test that banned user redirect to the banned page correctly
        resp = self.client.post(reverse('imageboard_thread_create', kwargs={'board': self.board1.slug}), {'post': 'Im trying to break the rules!'})
        self.assertRedirects(resp, expected_url=reverse('dj-mod:moderation_ban_page'))
        resp2 = self.client.post(reverse('imageboard_userpost_create', kwargs={'board': self.board1.slug, 'thread_number': self.thread1.thread_number}), 
            {'post': 'Im trying to break the rules!'})
        self.assertRedirects(resp2, expected_url=reverse('dj-mod:moderation_ban_page'))
        

    def test_ban_page(self): #Test that ban page displays correctly
        resp = self.client.get(reverse('dj-mod:moderation_ban_page'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'moderation/transgression_detail.html')
        self.assertTrue('transgression_list' in resp.context)


class LoginViewTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user', password='pass')
  
    def test_login_view_get(self):
        resp = self.client.get(reverse('dj-mod:login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'moderation/login.html')

    def test_login_view_post(self):
        resp = self.client.post(reverse('dj-mod:login'), {'username': 'user', 'password': 'pass'})
        #self.assertRedirects(resp, expected_url=LOGIN_REDIRECT_URL, status_code=302)
    
    def test_user_context(self):
        self.client.login(username='user', password='pass')
        resp = self.client.get(reverse('dj-mod:login'))
        self.assertEqual(resp.context['user'], self.user1)

    def test_logout_get(self):
        resp = self.client.get(reverse('dj-mod:logout'))
        self.assertTemplateUsed(resp, 'moderation/logged_out.html')
        self.assertNotEqual(resp.context['user'], self.user1)

