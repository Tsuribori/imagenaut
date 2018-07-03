from django.urls import path
from .views import ThreadList, ThreadDetail
urlpatterns = [
    path('<slug:board>/<int:thread_number>/', ThreadDetail.as_view(), name='imageboard_thread_page'),  
    path('<slug:board>/', ThreadList.as_view(), name='imageboard_thread_list'),
]
