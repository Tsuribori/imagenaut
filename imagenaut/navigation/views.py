from django.shortcuts import render
from django.views.generic import ListView
from imageboard.models import Board, UserPost

class BoardList(ListView):
    model = Board
    context_object_name = 'board_list'
    template_name = 'navigation/board_list.html'

class Frontpage(ListView):
    template_name = 'navigation/frontpage.html'
    context_object_name = 'latest_posts'
    
    def get_queryset(self):
        return UserPost.objects.all().order_by('-time_made')[:5] 
