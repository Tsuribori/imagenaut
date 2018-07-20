from django.test import TestCase
from moderation.forms import TransgressionForm
from datetime import timedelta
from django.utils import timezone
class FormTestCase(TestCase):

    def test_trangression_form_validity(self):
        banned_until = timezone.now() + timedelta(days=1)
        form_data = {'banned_until': banned_until, 'reason': 'Rule breaking'}
        form = TransgressionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_transgression_blank_data(self):
        form = TransgressionForm(data={})
        self.assertFalse(form.is_valid())
        required = ['This field is required.']
        self.assertEqual(form.errors, {'banned_until':required, 'reason':required}) 
