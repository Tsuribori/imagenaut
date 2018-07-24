from django.shortcuts import get_object_or_404, redirect
from .models import Board, Thread
from .forms import ThreadForm, UserPostForm
from .utils import GetIPMixin, BanMixin
from django.views.generic import ListView, CreateView
# Create your views here.

class ThreadList(ListView):
    model = Thread
    context_object_name = 'thread_list'
    template_name = 'imageboard/board.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs): #Three lines of code to adhere to DRY and maybe optimize database access?
        self.desired_board = get_object_or_404(Board, slug=kwargs['board'])
        return super(ThreadList, self).dispatch(request, *args, **kwargs)
        
    def get_queryset(self):  #Show only threads that belong to the board requested
        return Thread.objects.filter(board=self.desired_board)

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['page_url'] = '?page='
       context['form'] = ThreadForm
       context['board'] = self.desired_board
       return context       

class ThreadDetail(ListView):
    model = Thread
    context_object_name = 'thread'
    template_name = 'imageboard/thread.html' 
    def get_queryset(self):
        return get_object_or_404(Thread, thread_number=self.kwargs['thread_number'])
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['form'] = UserPostForm
       return context   

class ThreadCreate(CreateView, GetIPMixin, BanMixin):
    form_class = ThreadForm
    template_name = 'imageboard/userpost_form_page.html'

    def dispatch(self, request, *args, **kwargs): #Check if the user is banned, redirect if true
        if self.user_is_banned():
            return redirect('moderation_ban_page')
        else:
            return super(ThreadCreate, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.ip_address = self.get_remote_address()
        form.instance.board = get_object_or_404(Board, slug=self.kwargs['board'])
        return super(ThreadCreate, self).form_valid(form)

class UserPostCreate(CreateView, GetIPMixin, BanMixin):
    form_class = UserPostForm
    template_name = 'imageboard/userpost_form_page.html'

    def dispatch(self, request, *args, **kwargs): #Check if the user is banned, redirect if true
        if self.user_is_banned():
            return redirect('moderation_ban_page')
        else:
            return super(UserPostCreate, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.ip_address = self.get_remote_address()
        form.instance.thread = get_object_or_404(Thread, thread_number=self.kwargs['thread_number'])
        return super(UserPostCreate, self).form_valid(form)
   
