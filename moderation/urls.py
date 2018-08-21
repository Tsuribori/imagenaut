from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from .views import ThreadBanCreate, UserPostBanCreate, TransgressionList, ReportedThreadList, ReportedUserPostList

urlpatterns = [
    path('thread/<int:thread_number>/ban/', ThreadBanCreate.as_view(), name='moderation_thread_ban'),
    path('post/<int:post_number>/ban/', UserPostBanCreate.as_view(), name='moderation_userpost_ban'),
    path('reports/threads/', ReportedThreadList.as_view(), name='moderation_thread_report_list'),
    path('reports/posts/', ReportedUserPostList.as_view(), name='moderation_userpost_report_list'), 
    path('banned/', TransgressionList.as_view(), name='moderation_ban_page'),
    path('login/', auth_views.login, {'template_name': 'moderation/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'template_name': 'moderation/logged_out.html', 'extra_context': {'form': AuthenticationForm}}, name='logout'),
    path('', RedirectView.as_view(pattern_name='dj-mod:moderation_ban_page', permanent=False))

] 
