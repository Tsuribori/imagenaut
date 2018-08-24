from django.test import TestCase
from datetime import timedelta
from django.utils import timezone
from seed.factories import BoardFactory, TransgressionFactory
# Create your tests here.

class ModelTestCase(TestCase):
  
    def setUp(self):
        future = timezone.now() + timedelta(days=1)
        self.board = BoardFactory()
        self.ban1 = TransgressionFactory(banned_from=self.board, banned_until=future)
    
    def test_no_global_ban(self):
        self.assertFalse(self.ban1.global_ban)
 
    def test_board_specific_ban(self):
        self.assertEqual(self.ban1.banned_from, self.board)    
    
    def test_future(self): #Test that ban is in future
        self.assertGreater(self.ban1.banned_until, timezone.now())
    
    def test_str(self): #Test the str method
        self.assertEqual(self.ban1.__str__(), "{}: {}".format(self.ban1.ip_address, self.ban1.banned_until))
