from rest_framework.test import APITestCase
from captcha.models import CaptchaStore
from django.conf import settings
from django.test import tag
from django.utils import timezone
from rest_framework.reverse import reverse
from api.serializers import BoardSerializer, ThreadSerializer, UserPostSerializer
from seed.factories import faker, BoardFactory, ThreadFactory, UserPostFactory, ImageFactory, TransgressionFactory

@tag('api')
class BoardViewListSet(APITestCase):

    def setUp(self): 
        self.boards = BoardFactory.create_batch(5)
        self.list_resp = self.client.get(reverse('api_board-list')) 
        self.board = BoardFactory()
        self.url = reverse('api_board-detail', kwargs={'slug': self.board.slug})
        self.detail_resp = self.client.get(self.url)
        self.post_data = {'name': faker.word(), 'description': faker.word(), 'slug': faker.word()}

    def test_list_view_status(self):
        self.assertEqual(self.list_resp.status_code, 200)

    def test_list_view_content(self):
        serializer_data = BoardSerializer(instance=self.boards, context={'request': self.list_resp.wsgi_request}, many=True).data
        self.assertEqual(self.list_resp.data, serializer_data)

    def test_detail_view_status(self):
        self.assertEqual(self.list_resp.status_code, 200)
    
    def test_detail_view_content(self):
        serializer_data = BoardSerializer(instance=self.board, context={'request': self.detail_resp.wsgi_request}).data
        self.assertEqual(self.detail_resp.data, serializer_data)

    def test_delete_permission(self):
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_post_permission(self):
        resp = self.client.post(self.url, self.post_data)
        self.assertEqual(resp.status_code, 403)

    def test_patch_permission(self):
        resp = self.client.patch(self.url, self.post_data)
        self.assertEqual(resp.status_code, 403)

    def test_put_permission(self):
        resp = self.client.put(self.url, self.post_data)
        self.assertEqual(resp.status_code, 403)


@tag('api')
class ThreadViewListSet(APITestCase):

    def setUp(self):
        self.board = BoardFactory()
        self.threads = ThreadFactory.create_batch(5, board=self.board)
        self.list_resp = self.client.get(reverse('api_thread-list'))
        self.thread = ThreadFactory()
        self.url = reverse('api_thread-detail', kwargs={'thread_number': self.thread.thread_number})
        self.detail_resp = self.client.get(self.url)
        
    def test_list_view_status(self):
        self.assertEqual(self.list_resp.status_code, 200)

    def test_list_view_content(self):
        #Have to reverse the data in self.threads because it's reverse to the responese order in relation to thread_number
        threads = self.threads[::-1]
        serializer_data = ThreadSerializer(instance=threads, context={'request': self.list_resp.wsgi_request}, many=True).data
        self.assertEqual(self.list_resp.data, serializer_data)

    def test_detail_view_status(self):
        self.assertEqual(self.detail_resp.status_code, 200)
    
    def test_detail_view_content(self):
        serializer_data = ThreadSerializer(instance=self.thread, context={'request': self.detail_resp.wsgi_request}).data
        self.assertEqual(self.detail_resp.data, serializer_data)

    def test_delete_permission(self):
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_post_permission(self):
        resp = self.client.post(reverse('api_thread-list'), {})
        self.assertEqual(resp.status_code, 400)

    def test_patch_permission(self):
        resp = self.client.patch(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_put_permission(self):
        resp = self.client.put(self.url)
        self.assertEqual(resp.status_code, 403)

@tag('api')
class UserPostViewListSet(APITestCase):
 
    def setUp(self):
        self.thread = ThreadFactory()
        self.posts = UserPostFactory.create_batch(5, thread=self.thread)
        self.list_resp = self.client.get(reverse('api_post-list'))
        self.post = UserPostFactory(thread=self.thread)
        self.url = reverse('api_post-detail', kwargs={'post_number': self.post.post_number})
        self.detail_resp = self.client.get(self.url)

    def test_list_view_status(self):
        self.assertEqual(self.list_resp.status_code, 200)
        
    def test_list_view_content(self): 
        serializer_data = UserPostSerializer(instance=self.posts, context={'request': self.list_resp.wsgi_request}, many=True).data
        self.assertEqual(self.list_resp.data, serializer_data)

    def test_detail_view_status(self):
        self.assertEqual(self.detail_resp.status_code, 200)

    def test_detail_view_content(self):
        serializer_data = UserPostSerializer(instance=self.post, context={'request': self.detail_resp.wsgi_request}).data
        self.assertEqual(self.detail_resp.data, serializer_data)

    def test_delete_permission(self):
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_post_permission(self):
        resp = self.client.post(reverse('api_post-list'), {})
        self.assertEqual(resp.status_code, 400)

    def test_patch_permission(self):
        resp = self.client.patch(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_put_permission(self):
        resp = self.client.put(self.url)
        self.assertEqual(resp.status_code, 403)

@tag('api')
class ThreadViewListSetPOST(APITestCase):

    def setUp(self):
        self.board = BoardFactory()
        self.ip_address = '127.0.0.1'
        self.url = reverse('api_thread-list')
        get_captcha_resp = self.client.get(reverse('rest_validator_view'))
        self.key = get_captcha_resp.data['captcha_key']
        self.captcha_value = CaptchaStore.objects.get(hashkey=self.key).challenge
        validate_resp = self.client.post(reverse('rest_validator_view'), {'captcha_key': self.key, 'captcha_value': self.captcha_value})
        self.data = {
            'subject': faker.name(),
            'name': faker.name(),
            'post': faker.text(),
            'image': ImageFactory(),
            'board': reverse('api_board-detail', kwargs={'slug': self.board.slug}),
            'captcha_key': self.key,
        }

   
    def test_valid_post(self):
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, 201)  

    def test_invalid_captcha(self):
        self.data['captcha_key'] = faker.word()
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, 400)

    def test_global_banned_user(self):
       TransgressionFactory(ip_address=self.ip_address, global_ban=True)
       resp = self.client.post(self.url, self.data)
       self.assertEqual(resp.status_code, 400) 

    def test_board_banned_user(self):
        TransgressionFactory(ip_address=self.ip_address, banned_from=self.board)
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, 400)

    def test_user_on_cooldown(self):
       ThreadFactory(ip_address=self.ip_address)
       resp = self.client.post(self.url, self.data)
       self.assertEqual(resp.status_code, 400)

@tag('api')
class UserPostViewListSetPOST(APITestCase):

    def setUp(self):
        self.thread = ThreadFactory()
        self.ip_address = '127.0.0.1'
        self.url = reverse('api_post-list')
        get_captcha_resp = self.client.get(reverse('rest_validator_view'))
        self.key = get_captcha_resp.data['captcha_key']
        self.captcha_value = CaptchaStore.objects.get(hashkey=self.key).challenge
        validate_resp = self.client.post(reverse('rest_validator_view'), {'captcha_key': self.key, 'captcha_value': self.captcha_value})
        self.data = {
            'name': faker.name(),
            'post': faker.text(),
            'thread': reverse('api_thread-detail', kwargs={'thread_number': self.thread.thread_number}),
            'captcha_key': self.key,
        }

   
    def test_valid_post(self):
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, 201)  

    def test_invalid_captcha(self):
        self.data['captcha_key'] = faker.word()
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, 400)

    def test_global_banned_user(self):
       TransgressionFactory(ip_address=self.ip_address, global_ban=True)
       resp = self.client.post(self.url, self.data)
       self.assertEqual(resp.status_code, 400) 

    def test_board_banned_user(self):
        TransgressionFactory(ip_address=self.ip_address, banned_from=self.thread.board)
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, 400)

    def test_user_on_cooldown(self):
       UserPostFactory(ip_address=self.ip_address)
       resp = self.client.post(self.url, self.data)
       self.assertEqual(resp.status_code, 400)

