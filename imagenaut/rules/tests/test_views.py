from django.test import TestCase
from django.urls import reverse
from seed.factories import BoardFactory, RuleFactory
from rules.models import Rule

class RuleListTestCase(TestCase):
    
    def setUp(self):
        self.boards = BoardFactory.create_batch(5)
        for board in self.boards:
            RuleFactory.create_batch(2, board=board)
        self.global_rules = RuleFactory.create_batch(2, board=None)
        self.resp = self.client.get(reverse('rules_rule_list'))
        self.global_rule_query = Rule.objects.filter(board=None) #Must do this to bypass ordering shenanigans

    def test_status_code(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'rules/rule_list.html')

    def test_global_rule_context(self):
        self.assertTrue('global_rules' in self.resp.context)

    def test_board_list_context(self):
        self.assertTrue('board_list' in self.resp.context)

    def test_page_contains_global_rules(self):
        for rule in self.global_rules:
            self.assertContains(self.resp, rule.text)

    def test_page_contains_board_rules(self):
        for board in self.boards:
            for rule in board.rules.all():
                self.assertContains(self.resp, rule.text)

