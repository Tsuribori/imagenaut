from django.shortcuts import get_object_or_404
from .models import Board, Thread
from django.views.generic import ListView, DetailView

# Create your views here.

class ThreadList(ListView):
    model = Thread
    context_object_name = 'thread_list'
    template_name = 'imageboard/board.html'
    
    def get_queryset(self):
        desired_board = get_object_or_404(Board, slug=self.kwargs['board'])
        return Thread.objects.filter(board=desired_board)

class ThreadDetail(ListView):
    model = Thread
    context_object_name = 'thread'
    template_name = 'imageboard/thread.html'
    def get_queryset(self):
        return get_object_or_404(Thread, thread_number=self.kwargs['thread_number'])
        
