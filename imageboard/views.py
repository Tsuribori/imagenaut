from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Prefetch
from .models import Board, Thread, UserPost
from .forms import ThreadForm, UserPostForm
from .utils import GetIPMixin, BanMixin, CooldownMixin
from django.views.generic import View, ListView, CreateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
# Create your views here.

class ThreadList(ListView):
    model = Thread
    context_object_name = 'thread_list'
    template_name = 'imageboard/board.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs): #Three lines of code to adhere to DRY and maybe optimize database access?
        self.desired_board = get_object_or_404(Board.objects.prefetch_related(
            Prefetch('threads', queryset=Thread.objects.filter(archived=False), to_attr='cached_threads')), slug=kwargs['board'])
        return super(ThreadList, self).dispatch(request, *args, **kwargs)
        
    def get_queryset(self):  #Show only threads that belong to the board requested 
        return self.desired_board.cached_threads

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['page_url'] = '?page='
       context['form'] = ThreadForm
       context['board'] = self.desired_board
       context['moderation_view'] = False
       return context       

class ThreadDetail(ListView):
    model = Thread
    context_object_name = 'thread'
    template_name = 'imageboard/thread.html' 
    def get_queryset(self):
        return get_object_or_404(Thread.objects.prefetch_related(Prefetch('posts', to_attr='cached_posts')), thread_number=self.kwargs['thread_number'])
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['form'] = UserPostForm
       return context   

class ThreadCreate(CreateView, GetIPMixin, BanMixin, CooldownMixin):
    form_class = ThreadForm
    template_name = 'imageboard/thread_form_page.html'

    def dispatch(self, request, *args, **kwargs): #Check if the user is banned, redirect if true
        self.board = get_object_or_404(Board, slug=kwargs['board'])
        if self.user_is_banned(self.board):
            return redirect('dj-mod:moderation_ban_page')
        else:
            return super(ThreadCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        return context

    def get_form_kwargs(self):
        kwargs = super(ThreadCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    def form_valid(self, form):
        form.instance.ip_address = self.get_remote_address()
        form.instance.board = self.board
        return super(ThreadCreate, self).form_valid(form)

class UserPostCreate(CreateView, GetIPMixin, BanMixin, CooldownMixin):
    form_class = UserPostForm
    template_name = 'imageboard/userpost_form_page.html'

    def dispatch(self, request, *args, **kwargs): #Check if the user is banned, redirect if true
        self.thread = get_object_or_404(Thread, thread_number=kwargs['thread_number'])
        if self.user_is_banned(self.thread.board):
            return redirect('dj-mod:moderation_ban_page')
        else:
            return super(UserPostCreate, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thread'] = self.thread
        return context    

    def get_form_kwargs(self):
        kwargs = super(UserPostCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        form.instance.ip_address = self.get_remote_address()
        form.instance.thread = self.thread
        return super(UserPostCreate, self).form_valid(form)

class ThreadDelete(PermissionRequiredMixin, DeleteView):
    model = Thread
    template_name = 'imageboard/thread_confirm_delete.html'
    permission_required = 'imageboard.delete_thread'
    raise_exception = True
   
    def dispatch(self, request, *args, **kwargs): 
        self.thread = get_object_or_404(Thread, thread_number=kwargs['thread_number'])
        return super(ThreadDelete, self).dispatch(request, *args, **kwargs) 
   
    def get_object(self):
        return self.thread

    def get_success_url(self):
        return self.thread.board.get_absolute_url()

class UserPostDelete(PermissionRequiredMixin, DeleteView):
    model = UserPost
    template_name = 'imageboard/userpost_confirm_delete.html'
    permission_required = 'imageboard.delete_userpost'
    raise_exception = True
 
    def dispatch(self, request, *args, **kwargs): 
        self.userpost = get_object_or_404(UserPost, post_number=kwargs['post_number'])
        return super(UserPostDelete, self).dispatch(request, *args, **kwargs)
        
    def get_object(self):
        return self.userpost
    
    def get_success_url(self):
        return self.userpost.thread.get_absolute_url()

class ThreadReport(View):
    template_name = 'imageboard/thread_report_confirm.html'

    def get(self, request, *args, **kwargs):
        thread = get_object_or_404(Thread, thread_number=kwargs['thread_number'])
        return render(request, self.template_name,  {'thread': thread})

    def post(self, request, *args, **kwargs):
        thread = get_object_or_404(Thread, thread_number=kwargs['thread_number'])
        thread.reported = True
        thread.save()
        return redirect(thread)

class UserPostReport(View):
    template_name = 'imageboard/userpost_report_confirm.html'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(UserPost, post_number=kwargs['post_number'])
        return render(request, self.template_name, {'userpost': post})

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(UserPost, post_number=kwargs['post_number'])
        post.reported = True
        post.save()
        return redirect(post)


