from django.shortcuts import get_object_or_404
from imageboard.models import Board, Thread

class ArchiveMixin():
    date_field = 'time_made'
    make_object_list = True
    context_object_name = 'thread_list'
    template_name = 'archives/archive_list.html'
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):
        self.board = get_object_or_404(Board, slug=self.kwargs['board'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.board.threads.filter(archived=True).prefetch_related('board', 'posts')

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['page_url'] = '?page='
       context['moderation_view'] = False
       return context

