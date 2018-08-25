from django.shortcuts import render
from django.views.generic import ListView
from .models import Rule
from imageboard.models import Board


class RuleList(ListView):
    context_object_name = 'board_list'
    template_name = 'rules/rule_list.html'

    def get_queryset(self):
        return Board.objects.all().prefetch_related('rules')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['global_rules'] = Rule.objects.filter(board=None)
        return context
