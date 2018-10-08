import urllib
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Q
from .forms import ArchiveSearchForm
from imageboard.models import Board, Thread

class ArchiveMixin():
    date_field = 'time_made'
    make_object_list = True
    allow_empty = True
    context_object_name = 'thread_list'
    template_name = 'archives/archive_list.html'
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):
        self.board = get_object_or_404(Board.objects.prefetch_related(
            Prefetch('threads', queryset=Thread.objects.filter(archived=True).prefetch_related('board', 'posts'))),
            slug=self.kwargs['board'])
        self.search_term = request.GET.get('search')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_term:
            self.search_term = urllib.parse.unquote(self.search_term)
            return self.board.threads.filter(
                Q(subject__icontains=self.search_term) | Q(post__icontains=self.search_term), archived=True).prefetch_related('posts')
        return self.board.threads

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['page_url'] = '?page='
       context['moderation_view'] = False
       context['form'] = ArchiveSearchForm
       return context

