from django.urls import path
from .views import ThreadBanCreate, UserPostBanCreate
urlpatterns = [
    path('thread/<int:thread_number>/ban/', ThreadBanCreate.as_view(), name='moderation_thread_ban'),
    #path('thread/<int:thread_number>/delete/', name='moderation_thread_delete'), 
    path('post/<int:post_number>/ban/', UserPostBanCreate.as_view(), name='moderation_userpost_ban'),
    #path('post/<int:post_number>/delete', name='moderation_userpost_delet'),
] 
