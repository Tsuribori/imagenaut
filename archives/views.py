from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.views.generic import ListView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView
from .utils import ArchiveMixin
from imageboard.models import Thread, Board

class ThreadArchive(ListView):
   model = Thread
   context_object_name = 'thread_list'
   template_name = 'archives/archive_list.html'
   paginate_by = 50
   
   def dispatch(self, request, *args, **kwargs): 
       self.desired_board = get_object_or_404(Board.objects.prefetch_related(
           Prefetch('threads', queryset=Thread.objects.filter(archived=True).prefetch_related('board', 'posts'), to_attr='cached_threads')), slug=kwargs['board'])
       return super(ThreadArchive, self).dispatch(request, *args, **kwargs)

   def get_queryset(self):
       return self.desired_board.cached_threads

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['page_url'] = '?page='
       context['moderation_view'] = False
       return context

class ThreadYearArchive(ArchiveMixin, YearArchiveView):
    pass
   
class ThreadMonthArchive(ArchiveMixin, MonthArchiveView):
    pass

class ThreadDayArchive(ArchiveMixin, DayArchiveView):
    pass
