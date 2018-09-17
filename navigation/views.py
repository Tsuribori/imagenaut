from django.shortcuts import render
from django.views.generic import ListView
from imageboard.models import Board

class BoardList(ListView):
    model = Board
    context_object_name = 'board_list'
    template_name = 'navigation/board_list.html'
 
