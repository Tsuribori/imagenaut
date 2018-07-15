from django.urls import path
from .views import ThreadList, ThreadDetail, ThreadCreate, UserPostCreate
urlpatterns = [
    path('<slug:board>/<int:thread_number>/create/', UserPostCreate.as_view(), name='imageboard_userpost_create'),
    path('<slug:board>/<int:thread_number>/', ThreadDetail.as_view(), name='imageboard_thread_page'),
    path('<slug:board>/create/', ThreadCreate.as_view(), name='imageboard_thread_create'),  
    path('<slug:board>/', ThreadList.as_view(), name='imageboard_thread_list'),
    
]
