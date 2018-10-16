from rest_framework.test import APITestCase
from django.test import tag
from rest_framework.reverse import reverse
from api.serializers import BoardSerializer, ThreadSerializer
from seed.factories import faker, BoardFactory, ThreadFactory

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
        self.detail_resp = self.client.get(reverse('api_thread-detail', kwargs={'thread_number': self.thread.thread_number}))

    def test_list_view_status(self):
        self.assertEqual(self.list_resp.status_code, 200)

    def test_list_view_content(self):
        #Have to reverse the data in self.threads because it's reverse to the responese order in relation to thread_number
        threads = self.threads[::-1]
        serializer_data = ThreadSerializer(instance=threads, context={'request': self.list_resp.wsgi_request}, many=True).data
        self.assertEqual(self.list_resp.data, serializer_data)

    def test_detail_view_status(self):
        self.assertEqual(self.list_resp.status_code, 200)
    
    def test_detail_view_content(self):
        serializer_data = ThreadSerializer(instance=self.thread, context={'request': self.detail_resp.wsgi_request}).data
        self.assertEqual(self.detail_resp.data, serializer_data)

