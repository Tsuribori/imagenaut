from django.urls import reverse
from django.test import TestCase, tag
from archives.forms import ArchiveSearchForm
from seed.factories import faker, BoardFactory, ThreadFactory, DateFactory

#There are several almost identical tests in this page. This is to futureproof for potential changes to views and also due to clumsy pagination

@tag('archive')
class ArchiveSearchTestCase(TestCase):

    def setUp(self):
        self.resp = self.client.get(reverse('archive_search_form'))

    def test_status(self):
        self.assertEqual(self.resp.status_code, 200)
 
    def test_template(self):
        self.assertTemplateUsed(self.resp, 'archives/search_page.html')

    def test_form_context(self):
        self.assertTrue('form' in self.resp.context)

#Test that the search feature works correctly and only displays archived threads
@tag('archive')
class ArchiveSearchTerm(TestCase):

    def setUp(self):
        self.board = BoardFactory()
        self.thread = ThreadFactory(archived=True, board=self.board)
        self.thread2 = ThreadFactory(archived=False, board=self.board)
        self.subject_resp = self.client.post(reverse('archive_search_form'), {'board': self.board, 'search_term': self.thread.subject}, follow=True)
        self.subject_resp2 = self.client.post(reverse('archive_search_form'), {'board': self.board, 'search_term': self.thread2.subject}, follow=True)
        self.post_resp = self.client.post(reverse('archive_search_form'), {'board': self.board, 'search_term': self.thread.post}, follow=True)
        self.post_resp2 = self.client.post(reverse('archive_search_form'), {'board': self.board, 'search_term': self.thread2.post}, follow=True)

    def test_search_by_subject(self):
        self.assertContains(self.subject_resp, self.thread.subject)
   
    def test_search_by_subject_not_archived(self):
        self.assertNotContains(self.subject_resp2, self.thread2.subject)

    def test_search_by_post(self):
        self.assertContains(self.post_resp, self.thread.post)

    def test_search_by_post_not_archived(self):
        self.assertNotContains(self.post_resp2, self.thread2.post)

#Similar test to above but on the date views, which have different logic that the archive list for only boards
@tag('archive')
class ArchiveSearchTermDate(TestCase):
    
    def setUp(self):
        self.board = BoardFactory()
        self.thread = ThreadFactory(archived=True, board=self.board)
        self.thread2 = ThreadFactory(archived=False, board=self.board)
        self.subject_resp = self.client.post(reverse('archive_search_form'), {
            'board': self.board, 'year': self.thread.time_made.year, 'search_term': self.thread.subject}, follow=True)
        self.subject_resp2 = self.client.post(reverse('archive_search_form'), {
            'board': self.board, 'year': self.thread.time_made.year, 'search_term': self.thread2.subject}, follow=True)
        self.post_resp = self.client.post(reverse('archive_search_form'), {
            'board': self.board, 'year': self.thread2.time_made.year, 'search_term': self.thread.post}, follow=True)
        self.post_resp2 = self.client.post(reverse('archive_search_form'), {
            'board': self.board, 'year': self.thread2.time_made.year, 'search_term': self.thread2.post}, follow=True)

    def test_search_by_subject(self):
        self.assertContains(self.subject_resp, self.thread.subject)
   
    def test_search_by_subject_not_archived(self):
        self.assertNotContains(self.subject_resp2, self.thread2.subject)

    def test_search_by_post(self):
        self.assertContains(self.post_resp, self.thread.post)

    def test_search_by_post_not_archived(self):
        self.assertNotContains(self.post_resp2, self.thread2.post)


#Test that submitting a form redirects correctly based on the values
@tag('archive')
class ArchiveSearchFormPost(TestCase):

    def setUp(self):
        self.board = BoardFactory()
        self.thread = ThreadFactory(time_made=DateFactory.last_year(), archived=True, board=self.board)
        self.time = self.thread.time_made

    def test_board_url(self):
        resp = self.client.post(reverse('archive_search_form'), {'board': self.board.name})
        self.assertRedirects(resp, expected_url=self.board.get_archive_url())
      
    def test_year_url(self):
        resp = self.client.post(reverse('archive_search_form'), 
            {'board': self.board.name, 'year': self.time.year})
        self.assertRedirects(resp, expected_url=self.thread.get_archive_year_url())

    def test_month_url(self):
        resp = self.client.post(reverse('archive_search_form'),
            {'board': self.board.name, 'year': self.time.year, 'month': self.time.month})
        self.assertRedirects(resp, expected_url=self.thread.get_archive_month_url())

    def test_day_url(self):
        resp = self.client.post(reverse('archive_search_form'),
          {'board': self.board.name, 'year': self.time.year, 'month': self.time.month, 'day': self.time.day})  
        self.assertRedirects(resp, expected_url=self.thread.get_archive_day_url())

@tag('archive')
class ThreadArchiveTestCase(TestCase):

    def setUp(self):
        self.board = BoardFactory()
        self.threads = ThreadFactory.create_batch(5, board=self.board, archived=True)
        self.not_archived = ThreadFactory(board=self.board, archived=False)
        self.resp = self.client.get(self.board.get_archive_url()) 
       

    def test_status(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'archives/archive_list.html')

    def test_shows_archived(self):
        for thread in self.threads:
            self.assertContains(self.resp, thread.post)

    def test_doesnt_show_active(self):
        self.assertNotContains(self.resp, self.not_archived.post)

    def test_links(self):
        for thread in self.threads:
            self.assertContains(self.resp, thread.get_absolute_url())

    def test_context(self):
        self.assertFalse(self.resp.context['moderation_view'])

    def test_form_context(self):
        self.assertTrue('form' in self.resp.context)

@tag('archive')
class ThreadYearArchiveTest(TestCase):

    def setUp(self):
        last_year = DateFactory.last_year()
        self.board = BoardFactory()
        self.threads = ThreadFactory.create_batch(5, time_made=last_year, board=self.board, archived=True)
        self.not_archived = ThreadFactory(time_made=last_year, board=self.board, archived=False)
        self.resp = self.client.get(self.threads[0].get_archive_year_url())
       

    def test_status(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'archives/archive_list.html')

    def test_shows_archived(self):
        for thread in self.threads:
            self.assertContains(self.resp, thread.post)

    def test_doesnt_show_active(self):
        self.assertNotContains(self.resp, self.not_archived.post)

    def test_links(self):
        for thread in self.threads:
            self.assertContains(self.resp, thread.get_absolute_url())

    def test_context(self):
        self.assertFalse(self.resp.context['moderation_view'])

    def test_form_context(self):
        self.assertTrue('form' in self.resp.context)


@tag('archive')
class ThreadMonthArchiveTest(TestCase):
 
    def setUp(self):
        last_month = DateFactory.last_month()
        self.board = BoardFactory()
        self.threads = ThreadFactory.create_batch(5, time_made=last_month, board=self.board, archived=True)
        self.not_archived = ThreadFactory(time_made=last_month, board=self.board, archived=False)
        self.resp = self.client.get(self.threads[0].get_archive_month_url())

    def test_status(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'archives/archive_list.html')

    def test_shows_archived(self):
        for thread in self.threads:
            self.assertContains(self.resp, thread.post)

    def test_doesnt_show_active(self):
        self.assertNotContains(self.resp, self.not_archived.post)

    def test_links(self):
        for thread in self.threads:
            self.assertContains(self.resp, thread.get_absolute_url())

    def test_context(self):
        self.assertFalse(self.resp.context['moderation_view'])

    def test_form_context(self):
        self.assertTrue('form' in self.resp.context)

@tag('archive')
class ThreadDayArchiveTest(TestCase):

    def setUp(self):
        yesterday = DateFactory.yesterday()
        self.board = BoardFactory()
        self.threads = ThreadFactory.create_batch(5, time_made=yesterday, board=self.board, archived=True)
        self.not_archived = ThreadFactory(time_made=yesterday, board=self.board, archived=False)
        self.resp = self.client.get(self.threads[0].get_archive_day_url())

    def test_status(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'archives/archive_list.html')

    def test_shows_archived(self):
        for thread in self.threads:
            self.assertContains(self.resp, thread.post)

    def test_doesnt_show_active(self):
        self.assertNotContains(self.resp, self.not_archived.post)

    def test_links(self):
        for thread in self.threads:
            self.assertContains(self.resp, thread.get_absolute_url())

    def test_context(self):
        self.assertFalse(self.resp.context['moderation_view'])

    def test_form_context(self):
        self.assertTrue('form' in self.resp.context)


@tag('archive', 'slow')
class ThreadArchivePagination(TestCase):
    
    def setUp(self):
        last_year = DateFactory.last_year()
        self.board = BoardFactory()
        self.thread = ThreadFactory(time_made=last_year, board=self.board, archived=True)
        self.threads = ThreadFactory.create_batch(50, time_made=last_year, board=self.board, archived=True)
        self.first_page = self.client.get(self.board.get_archive_url())
        self.second_page = self.client.get('{}?page=2'.format(self.board.get_archive_url()))

    def test_first_page(self):
        for thread in self.threads:
            self.assertContains(self.first_page, thread.post)
    
    def test_first_page_not_contains(self):
        self.assertNotContains(self.first_page, self.thread.post)

    def test_second_page(self):
        self.assertContains(self.second_page, self.thread.post)

    def test_second_page_not_contains(self):
        for thread in self.threads:
            self.assertNotContains(self.second_page, thread.post)

    def test_page_url(self):
        self.assertContains(self.first_page, '?page=2')

@tag('archive', 'slow')
class ThreadDatePagination(TestCase):

    def setUp(self):
        last_year = DateFactory.last_year()
        self.board = BoardFactory()
        self.thread = ThreadFactory(time_made=last_year, board=self.board, archived=True)
        self.threads = ThreadFactory.create_batch(50, time_made=last_year, board=self.board, archived=True)
        self.first_page = self.client.get(self.thread.get_archive_year_url())
        self.second_page = self.client.get('{}?page=2'.format(self.thread.get_archive_year_url()))

    def test_first_page(self):
        for thread in self.threads:
            self.assertContains(self.first_page, thread.post)
    
    def test_first_page_not_contains(self):
        self.assertNotContains(self.first_page, self.thread.post)

    def test_second_page(self):
        self.assertContains(self.second_page, self.thread.post)

    def test_second_page_not_contains(self):
        for thread in self.threads:
            self.assertNotContains(self.second_page, thread.post)

    def test_page_url(self):
        self.assertContains(self.first_page, '?page=2')
