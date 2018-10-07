from django.shortcuts import get_object_or_404, redirect
from django.db.models import Prefetch
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView
from .utils import ArchiveMixin
from .forms import ArchiveSearchForm 
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
       context['form'] = ArchiveSearchForm
       return context

class ThreadYearArchive(ArchiveMixin, YearArchiveView):
    pass
   
class ThreadMonthArchive(ArchiveMixin, MonthArchiveView):
    pass

class ThreadDayArchive(ArchiveMixin, DayArchiveView):
    pass

class ArchiveSearch(FormView):
     template_name = 'archives/search_page.html'
     form_class = ArchiveSearchForm

     def form_valid(self, form):
         year = form.cleaned_data['year']
         month = form.cleaned_data['month']
         day = form.cleaned_data['day']
         board = get_object_or_404(Board, name=form.cleaned_data['board'])
         if day:
             return redirect(reverse('archive_thread_day_list', kwargs={
                 'board': board.slug, 'year': year, 'month': month, 'day': day}))
         elif month:
             return redirect(reverse('archive_thread_month_list', kwargs={
                 'board': board.slug, 'year': year, 'month': month}))
         elif year:
             return redirect(reverse('archive_thread_year_list', kwargs={
                 'board': board.slug, 'year': year}))
             
         return redirect(board.get_archive_url())
         
