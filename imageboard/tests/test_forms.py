from django.test import TestCase
from imageboard.forms import ThreadForm, UserPostForm
from seed.factories import ImageFactory

class FormsTestCase(TestCase):
    
    def test_thread_form_validity(self):
        form_data = {'post': 'Test123', 'name': 'Johnny', 'subject': 'This is a test'}
        form = ThreadForm(form_data, {'image': ImageFactory()})
        self.assertTrue(form.is_valid())
        
    
    def test_userpost_form_validity(self):
        form_data = {'post': 'Test123', 'name': 'Johnny'}
        form = UserPostForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_thread_blank_data(self):
        form = ThreadForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, 
            {'post': ['This field is required.'], 'name': ['This field is required.'], 'image': ['This field is required.']})

    def test_userpost_blank_data(self):
        form = UserPostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'post': ['This field is required.'], 'name': ['This field is required.']}) 
