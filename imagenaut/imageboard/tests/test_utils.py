from django.test import TestCase, tag
from django.urls import reverse
from seed.factories import faker, BoardFactory, ThreadFactory, UserPostFactory, TransgressionFactory 
from imageboard.utils import GetIPMixin, BanMixin, CooldownMixin
from imageboard.models import Thread, UserPost


class GetIPMixinTestCase(TestCase, GetIPMixin):
    
    def setUp(self):
       self.board = BoardFactory()
       
    def test_get_ip_valid_request(self):
        resp = self.client.post(reverse('imageboard_thread_create', kwargs={'board': self.board.slug}), 
            {'post': faker.text(), 'name': faker.name()})
        self.request = resp.wsgi_request #get_remote_address only gets the ip through a self.request object so one must be provided
        remote_address = self.get_remote_address()
        self.assertEqual(remote_address, '127.0.0.1')
    
    def test_get_ip_no_valid_request(self):
        resp = self.client.post(reverse('imageboard_thread_create', kwargs={'board': self.board.slug}),
             {'post': faker.text(), 'name': faker.name()})
        remote_address = self.get_remote_address()
        self.assertEqual(remote_address, None) #Test that None is returned if no request object provided
    

class BanMixinTestCase(TestCase, GetIPMixin, BanMixin):

    def setUp(self):
        self.board = BoardFactory()
        self.board2 = BoardFactory()
        resp = self.client.get(reverse('dj-mod:login'))
        self.request = resp.wsgi_request 
        self.thread = ThreadFactory(ip_address=self.get_remote_address())
       
    
    def test_ban_false(self):
        self.assertFalse(self.user_is_banned(self.board))

    def test_global_ban_true(self):
        ban = TransgressionFactory(ip_address=self.thread.ip_address, global_ban=True)
        self.assertTrue(self.user_is_banned(self.board))

    def test_board_ban_true(self):
        ban = TransgressionFactory(ip_address=self.thread.ip_address, banned_from=self.board)
        self.assertTrue(self.user_is_banned(self.board))

    def test_ban_in_another_board(self):
        ban = TransgressionFactory(ip_address=self.thread.ip_address, banned_from=self.board2)
        self.assertFalse(self.user_is_banned(self.board))

class CooldownMixinTestCase(TestCase, GetIPMixin, CooldownMixin):
    
    def setUp(self):
        resp = self.client.get(reverse('dj-mod:login'))
        self.request = resp.wsgi_request
        self.board = BoardFactory()
    
    def test_cooldown_false(self):
        self.assertFalse(self.user_on_cooldown(Thread))
        self.assertFalse(self.user_on_cooldown(UserPost))
 
    def test_cooldown_true(self):
        thread = ThreadFactory(ip_address=self.get_remote_address())
        post = UserPostFactory(ip_address=self.get_remote_address())
        self.assertTrue(self.user_on_cooldown(Thread))
        self.assertTrue(self.user_on_cooldown(UserPost))

