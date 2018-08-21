from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Prefetch
from .models import Transgression
from imageboard.models import Board, Thread, UserPost
from imageboard.utils import GetIPMixin #IP needed for ban page
from .forms import TransgressionForm
from django.views.generic import CreateView, ListView
# Create your views here.

class ThreadBanCreate(CreateView):
    form_class = TransgressionForm
    template_name = 'moderation/transgression_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.thread = get_object_or_404(Thread, thread_number=self.kwargs['thread_number'])
        return super(ThreadBanCreate, self).dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return self.thread.get_absolute_url()

    def form_valid(self, form):
        form.instance.ip_address = self.thread.ip_address
        if form.instance.global_ban == False:
            form.instance.banned_from = self.thread.board
        return super(ThreadBanCreate, self).form_valid(form)

class UserPostBanCreate(CreateView):
    form_class = TransgressionForm
    template_name = 'moderation/transgression_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.userpost = get_object_or_404(UserPost, post_number=self.kwargs['post_number'])
        return super(UserPostBanCreate, self).dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return self.userpost.get_absolute_url()

    def form_valid(self, form):
        form.instance.ip_address = self.userpost.ip_address
        if form.instance.global_ban == False:
            form.instance.banned_from = self.userpost.thread.board
        return super(UserPostBanCreate, self).form_valid(form)

class TransgressionList(ListView, GetIPMixin): #Ban page that shows user bans
    model = Transgression
    context_object_name = 'transgression_list'
    template_name = 'moderation/transgression_detail.html'

    def get_queryset(self):
        ip_address = self.get_remote_address()
        return Transgression.objects.filter(ip_address__iexact=ip_address)

class ReportedThreadList(ListView):
    model = Thread
    context_object_name = 'thread_list'
    template_name = 'imageboard/board.html'
    paginate_by = 150

    def dispatch(self, request, *args, **kwargs):
        self.board = request.GET.get('board', None)
        if self.board:
            self.desired_board = get_object_or_404(Board.objects.prefetch_related(
                Prefetch('threads', queryset=Thread.objects.filter(reported=True), to_attr='cached_threads')), slug=self.board)
        return super(ReportedThreadList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.board:
            return self.desired_board.cached_threads
        else:
            return Thread.objects.filter(reported=True)  
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_url'] = '?page='
        context['moderation_view'] = True
        if self.board:
            context['moderation_board_url'] = '?board={}'.format(self.board)
        return context
    

class ReportedUserPostList(ListView):
    model = UserPost
    context_object_name = 'post_list'
    template_name = 'moderation/reported_userpost_list.html'
    paginate_by = 150
    
    def dispatch(self, request, *args, **kwargs):
        self.board = request.GET.get('board', None)
        if self.board:
            self.desired_board = get_object_or_404(Board, slug=self.board) 
        return super(ReportedUserPostList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.board:
            posts = UserPost.objects.filter(thread__board=self.desired_board, reported=True)
            return posts
        else:
            return UserPost.objects.filter(reported=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_url'] = '?page='
        if self.board:
            context['moderation_board_url'] = '?board={}'.format(self.board)
        return context
