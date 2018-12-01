from django.test import TestCase, tag
from django.utils import timezone
from archives.forms import ArchiveSearchForm
from seed.factories import faker, BoardFactory, DateFactory

@tag('form', 'archive')
class ArchiveFormTest(TestCase):

    def setUp(self):
        self.current_year = timezone.now().year
        self.board = BoardFactory().name
   
    def test_valid_form(self): 
        form_data = {'board': self.board, 'year': self.current_year, 'month': DateFactory.month(), 'day': DateFactory.day_of_month(), 'search_term': faker.word()}
        form = ArchiveSearchForm(form_data)
        self.assertTrue(form.is_valid())

    def test_no_board(self):
        form_data = {'year': self.current_year, 'month': DateFactory.month(), 'day': DateFactory.day_of_month()}
        form = ArchiveSearchForm(form_data)
        self.assertFalse(form.is_valid())

    def test_no_year(self):
        form_data = {'board': self.board, 'month': DateFactory.month(), 'day': DateFactory.day_of_month()}
        form = ArchiveSearchForm(form_data)
        self.assertFalse(form.is_valid())

    def test_no_month(self):
        form_data = {'board': self.board, 'year': self.current_year, 'day': DateFactory.day_of_month()}
        form = ArchiveSearchForm(form_data)
        self.assertFalse(form.is_valid())
   
    def test_no_year_and_no_month(self):
        form_data = {'board': self.board, 'day': DateFactory.day_of_month()}
        form = ArchiveSearchForm(form_data)
        self.assertFalse(form.is_valid()) 

    def test_no_date(self):
        form_data = {'board': self.board}
        form = ArchiveSearchForm(form_data)
        self.assertTrue(form.is_valid())

    def test_url_encoded(self):
        form_data = {'board': self.board, 'search_term': '&'}
        form = ArchiveSearchForm(form_data)
        form.is_valid()
        self.assertEqual(form.cleaned_data['search_term'], '%26')
