from django.test import TestCase
from django.urls import reverse
from seed.factories import BoardFactory

class BoardList(TestCase):

    def setUp(self):
        self.boards = BoardFactory.create_batch(5)
        self.resp = self.client.get(reverse('navigation_board_list'))

    def test_status_code(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'navigation/board_list.html')

    def test_name(self):
        for board in self.boards:
            self.assertContains(self.resp, board.name)

    def test_description(self):
        for board in self.boards:
            self.assertContains(self.resp, board.description)
 
    def test_link(self):
        for board in self.boards:
            self.assertContains(self.resp, board.get_absolute_url())
