import json
from dateutil.parser import parse
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.test import tag
from api.serializers import BoardSerializer, ThreadSerializer
from seed.factories import BoardFactory, ThreadFactory

@tag('api')
class BoardSerializerTest(APITestCase):

    def setUp(self):
        self.board = BoardFactory()
        self.thread = ThreadFactory(board=self.board)
        self.resp = self.client.get(reverse('api_board-list')).wsgi_request
        self.data = BoardSerializer(instance=self.board, context={'request': self.resp}).data
 
           
 
    def test_url(self):
        self.assertEqual(self.data['url'], reverse('api_board-detail', kwargs={'slug': self.board.slug}, request=self.resp))

    def test_thread(self):
        self.assertEqual(self.data['threads'][0], reverse(
            'api_thread-detail', kwargs={'thread_number': self.thread.thread_number}, request=self.resp))

    def test_name(self):
        self.assertEqual(self.data['name'], self.board.name)

    def test_description(self):
        self.assertEqual(self.data['description'], self.board.description)

    def test_slug(self):
        self.assertEqual(self.data['slug'], self.board.slug)


@tag('api')
class ThreadSerializerTest(APITestCase):

    def setUp(self):
        self.thread = ThreadFactory()
        self.resp = self.client.get(reverse('api_thread-list')).wsgi_request
        self.data = ThreadSerializer(instance=self.thread, context={'request': self.resp}).data


    def test_url(self):
        self.assertEqual(self.data['url'], reverse(
            'api_thread-detail', kwargs={'thread_number': self.thread.thread_number}, request=self.resp))

    def test_thread_number(self):
        self.assertEqual(self.data['thread_number'], self.thread.thread_number)

    def test_subject(self):
        self.assertEqual(self.data['subject'], self.thread.subject)

    def test_name(self):
        self.assertEqual(self.data['name'], self.thread.name)
 
    def test_time_made(self):
        self.assertEqual(parse(self.data['time_made']), self.thread.time_made)

    def test_post(self):
        self.assertEqual(self.data['post'], self.thread.post)

    def test_board(self):
        self.assertEqual(self.data['board'], reverse(
            'api_board-detail', kwargs={'slug': self.thread.board.slug}, request=self.resp))

    def test_embed(self):
        self.assertEqual(self.data['embed'], self.thread.embed)

    def test_image(self):
        self.assertIn(self.thread.image.url, self.data['image'])

    def test_bumb_limit_reached(self):
        self.assertEqual(self.data['bumb_limit_reached'], self.thread.bumb_limit_reached)

    def test_archived(self):
        self.assertEqual(self.data['archived'], self.thread.archived)

    def test_pinned(self):
        self.assertEqual(self.data['pinned'], self.thread.pinned)
 
    def test_id_enabled(self):
        self.assertEqual(self.data['id_enabled'], self.thread.id_enabled)

    def test_poster_id(self):
        self.assertEqual(self.data['poster_id'], self.thread.poster_id)

    def test_reported(self):
        self.assertFalse(self.data.get('reported', False))

    def test_bumb_order(self):
        self.assertFalse(self.data.get('bumb_order', False))

    def test_ip_address(self):
        self.assertFalse(self.data.get('ip_address', False))

    
