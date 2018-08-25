from django.test import TestCase
from seed.factories import BoardFactory, RuleFactory

class RuleTestCase(TestCase):

   def setUp(self):
       self.board = BoardFactory()
       self.global_rule = RuleFactory(board=None)
       self.board_rule = RuleFactory(board=self.board) 

   def test_str(self):
       self.assertEqual(self.global_rule.__str__(), self.global_rule.text)

   def test_global_rule(self):
       self.assertEqual(self.global_rule.board, None)

   def test_board_rule(self):
       self.assertEqual(self.board_rule.board, self.board)

