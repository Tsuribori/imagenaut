from django.test import TestCase, tag
from seed.factories import faker, BoardFactory, ThreadFactory, DateFactory

#There are several almost identical tests in this page. This is to futureproof for potential changes to views and also due to clumsy pagination

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



@tag('archive')
class ThreadYearArchiveTest(TestCase):

    def setUp(self):
        last_year = DateFactory.last_year()
        self.board = BoardFactory()
        self.threads = ThreadFactory.create_batch(5, time_made=last_year, board=self.board, archived=True)
        self.not_archived = ThreadFactory(time_made=last_year, board=self.board, archived=False)
        self.resp = self.client.get('{}{}/'.format(self.board.get_archive_url(), last_year.year)) 
       

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


@tag('archive')
class ThreadMonthArchiveTest(TestCase):
 
    def setUp(self):
        last_month = DateFactory.last_month()
        self.board = BoardFactory()
        self.threads = ThreadFactory.create_batch(5, time_made=last_month, board=self.board, archived=True)
        self.not_archived = ThreadFactory(time_made=last_month, board=self.board, archived=False)
        self.resp = self.client.get('{}{}/{}/'.format(self.board.get_archive_url(), last_month.year, last_month.month)) 

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

@tag('archive')
class ThreadDayArchiveTest(TestCase):

    def setUp(self):
        yesterday = DateFactory.yesterday()
        self.board = BoardFactory()
        self.threads = ThreadFactory.create_batch(5, time_made=yesterday, board=self.board, archived=True)
        self.not_archived = ThreadFactory(time_made=yesterday, board=self.board, archived=False)
        self.resp = self.client.get('{}{}/{}/{}/'.format(self.board.get_archive_url(), yesterday.year, yesterday.month, yesterday.day)) 

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
        self.first_page = self.client.get('{}{}/'.format(self.board.get_archive_url(), last_year.year))
        self.second_page = self.client.get('{}{}/?page=2'.format(self.board.get_archive_url(), last_year.year))

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
