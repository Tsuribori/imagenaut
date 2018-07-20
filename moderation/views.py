from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from imageboard.models import Thread, UserPost
from .forms import TransgressionForm
from django.views.generic import CreateView
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
        return super(UserPostBanCreate, self).form_valid(form)

