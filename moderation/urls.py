from django.urls import path
from .views import ThreadBanCreate, UserPostBanCreate, TransgressionList
urlpatterns = [
    path('thread/<int:thread_number>/ban/', ThreadBanCreate.as_view(), name='moderation_thread_ban'),
    path('post/<int:post_number>/ban/', UserPostBanCreate.as_view(), name='moderation_userpost_ban'),
    path('banned/', TransgressionList.as_view(), name='moderation_ban_page'),
] 
