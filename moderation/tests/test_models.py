from django.test import TestCase
from datetime import timedelta
from django.utils import timezone
from moderation.models import Transgression
# Create your tests here.

class ModelTestCase(TestCase):
  
    def setUp(self):
        future = timezone.now() + timedelta(days=1)
        self.ban1 = Transgression.objects.create(ip_address='127.0.0.1', banned_until = future, reason='Breaking rules')
    
    def test_future(self): #Test that ban is in future
        self.assertGreater(self.ban1.banned_until, timezone.now())
    
    def test_str(self): #Test the str method
        self.assertEqual(self.ban1.__str__(), "{}: {}".format(self.ban1.ip_address, self.ban1.banned_until))
