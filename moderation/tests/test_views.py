from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from datetime import timedelta
from time import sleep
from django.conf import settings
from imageboard.models import Board, Thread, UserPost
from moderation.models import Transgression
from seed.factories import BoardFactory, ThreadFactory, UserPostFactory, TransgressionFactory

class BanViewTestCase(TestCase):
    
    def setUp(self):
        self.ip_addr = '127.0.0.1' 
        self.ban_data = {'banned_until':'2049-07-22', 'reason':'Breaking the rules.'}        
        self.board = BoardFactory()
        self.thread = ThreadFactory(board=self.board, ip_address=self.ip_addr)
        self.post = UserPostFactory(thread=self.thread, ip_address=self.ip_addr)
        self.old_THREAD_COOLDOWN = settings.THREAD_COOLDOWN
        settings.THREAD_COOLDOWN = 0
        self.old_POST_COOLDOWN = settings.POST_COOLDOWN
        settings.POST_COOLDOWN = 0

    def tearDown(self):
        settings.THREAD_COOLDOWN = self.old_THREAD_COOLDOWN
        settings.POST_COOLDOWN = self.old_POST_COOLDOWN        

       

    def test_thread_ban_get(self):
        resp = self.client.get(reverse('dj-mod:moderation_thread_ban', kwargs={'thread_number':self.thread.thread_number}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'moderation/transgression_form.html')
        self.assertTrue('form' in resp.context)
        
    def test_thread_board_ban_post(self):
        resp = self.client.post(reverse('dj-mod:moderation_thread_ban', kwargs={'thread_number':self.thread.thread_number}), self.ban_data)
        self.assertEqual(resp.status_code, 302)
        new_ban = Transgression.objects.get(reason=self.ban_data['reason'])
        self.assertEqual(new_ban.reason, self.ban_data['reason']) 
        self.assertEqual(new_ban.ip_address, '127.0.0.1')
        self.assertEqual(new_ban.banned_from, self.board)

    def test_thread_global_ban_post(self):
        reason = TransgressionFactory.reason
        resp = self.client.post(self.thread.get_ban_url(), {'reason': reason, 'banned_until': TransgressionFactory.banned_until, 'global_ban': True})
        self.assertEqual(resp.status_code, 302)
        new_ban = Transgression.objects.get(reason=reason)
        self.assertEqual(new_ban.global_ban, True)
        self.assertEqual(new_ban.banned_from, None)

    def test_userpost_ban_get(self):
        resp = self.client.get(reverse('dj-mod:moderation_userpost_ban', kwargs={'post_number':self.post.post_number}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'moderation/transgression_form.html')
        self.assertTrue('form' in resp.context)

    def test_userpost_board_ban_post(self):
        resp = self.client.post(reverse('dj-mod:moderation_userpost_ban', kwargs={'post_number':self.post.post_number}), self.ban_data)
        self.assertEqual(resp.status_code, 302)
        new_ban = Transgression.objects.get(reason=self.ban_data['reason'])
        self.assertEqual(new_ban.reason, self.ban_data['reason']) 
        self.assertEqual(new_ban.ip_address, '127.0.0.1')
        self.assertEqual(new_ban.banned_from, self.board)

    def test_userpost_global_ban_post(self):
        reason = TransgressionFactory.reason
        resp = self.client.post(self.post.get_ban_url(), {'reason': reason, 'banned_until': TransgressionFactory.banned_until, 'global_ban': True})
        self.assertEqual(resp.status_code, 302)
        new_ban = Transgression.objects.get(reason=reason)
        self.assertEqual(new_ban.global_ban, True)
        self.assertEqual(new_ban.banned_from, None)

 
    def test_ban_page_redirect_global_ban(self): #Test that banned user redirect to the banned page correctly when user has global ban
        ban = TransgressionFactory(global_ban=True, ip_address=self.ip_addr)
        resp = self.client.post(self.board.get_thread_create_url(),
            {'post': 'Im trying to break the rules!', 'name': 'Anon'})
        self.assertRedirects(resp, expected_url=reverse('dj-mod:moderation_ban_page'))
        resp2 = self.client.post(self.thread.get_post_create_url(), 
            {'post': 'Im trying to break the rules!', 'name': 'Anon'})
        self.assertRedirects(resp2, expected_url=reverse('dj-mod:moderation_ban_page'))
        
    
    def test_ban_page_redirect_board_specific(self): #Test that banned user redirects to the banned page correctly when user has board specific ban
        ban = TransgressionFactory(banned_from=self.board, ip_address=self.ip_addr)
        resp = self.client.post(reverse('imageboard_thread_create', kwargs={'board': self.board.slug}), 
            {'post': 'Im trying to break the rules!', 'name': 'Anon'})
        self.assertRedirects(resp, expected_url=reverse('dj-mod:moderation_ban_page'))
        resp2 = self.client.post(reverse('imageboard_userpost_create', kwargs={'board': self.board.slug, 'thread_number': self.thread.thread_number}), 
            {'post': 'Im trying to break the rules!', 'name': 'Anon'})
        self.assertRedirects(resp2, expected_url=reverse('dj-mod:moderation_ban_page'))

    def test_no_ban_redirect(self): #Test that there is no redirect when user has a ban in another board
        board2 = BoardFactory()
        ban = TransgressionFactory(banned_from=board2, ip_address=self.ip_addr)
        resp = self.client.post(reverse('imageboard_thread_create', kwargs={'board': self.board.slug}), 
            {'post': 'Im not trying to break the rules!', 'name': 'Anon'})
        self.assertRedirects(resp, expected_url=reverse('imageboard_thread_page', kwargs={'board': self.board.slug, 'thread_number': 1}))
        resp2 = self.client.post(reverse('imageboard_userpost_create', kwargs={'board': self.board.slug, 'thread_number': self.thread.thread_number}), 
            {'post': 'Im not trying to break the rules!', 'name': 'Anon'})
        self.assertRedirects(resp2, expected_url=self.thread.get_absolute_url())
        

    def test_ban_page(self): #Test that ban page displays correctly
        bans = TransgressionFactory.create_batch(5, ip_address=self.ip_addr)
        resp = self.client.get(reverse('dj-mod:moderation_ban_page'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'moderation/transgression_detail.html')
        self.assertTrue('transgression_list' in resp.context)
        for ban in bans:
            self.assertContains(resp, ban.reason)

class BanProperRedirectTestCase(TestCase): #Test that there is no redirect when user was banned in the past but it has expired
    
    def setUp(self):
        self.ban1 = self.ip_addr = '127.0.0.1' 
        self.board1 = Board.objects.create(name='Test board', slug='test')
        self.thread1 = Thread.objects.create(post='Test thread!', board=self.board1, ip_address=self.ip_addr)
        self.post1 = UserPost.objects.create(post='JOHNNY GUITAR', thread=self.thread1, ip_address=self.ip_addr)
        self.ban1 = Transgression.objects.create(banned_until=timezone.now()+timedelta(seconds=0.1), reason='Not liking the mods!', ip_address=self.ip_addr)
        self.old_THREAD_COOLDOWN = settings.THREAD_COOLDOWN
        settings.THREAD_COOLDOWN = 0.05
        self.old_POST_COOLDOWN = settings.POST_COOLDOWN
        settings.POST_COOLDOWN = 0.05

    def tearDown(self):
        settings.THREAD_COOLDOWN = self.old_THREAD_COOLDOWN
        settings.POST_COOLDOWN = self.old_POST_COOLDOWN
    
    def test_no_thread_redirect(self):
        sleep(0.1)
        resp = self.client.post(reverse('imageboard_thread_create', kwargs={'board': self.board1.slug}), 
            {'post': 'Im not breaking the rules!', 'name': 'Anon'})
        self.assertRedirects(resp, expected_url=reverse('imageboard_thread_page', kwargs={'board': self.board1.slug, 'thread_number': 1}), status_code=302)

    def test_no_post_redirect(self):
        sleep(0.1)
        resp = self.client.post(reverse('imageboard_userpost_create', kwargs={'board': self.board1.slug, 'thread_number': self.thread1.thread_number}),
            {'post': 'Im not breaking the rules!', 'name': 'Anon'})
        self.assertRedirects(resp, expected_url=self.thread1.get_absolute_url(), status_code=302)


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

