from django.urls import path
from .views import ThreadList, ThreadDetail, ThreadCreate, UserPostCreate, ThreadDelete, UserPostDelete, ThreadReport, UserPostReport, ThreadCatalog, UserPostAJAX
urlpatterns = [
    path('ajax/<int:post_number>/', UserPostAJAX.as_view(), name='imageboard_userpost_ajax'),
    path('<slug:board>/<int:thread_number>/<int:post_number>/delete/', UserPostDelete.as_view(), name='imageboard_userpost_delete'),
    path('<slug:board>/<int:thread_number>/<int:post_number>/report/', UserPostReport.as_view(), name='imageboard_userpost_report'),
    path('<slug:board>/<int:thread_number>/create/', UserPostCreate.as_view(), name='imageboard_userpost_create'),
    path('<slug:board>/<int:thread_number>/delete/', ThreadDelete.as_view(), name='imageboard_thread_delete'),
    path('<slug:board>/<int:thread_number>/report/', ThreadReport.as_view(), name='imageboard_thread_report'),
    path('<slug:board>/<int:thread_number>/', ThreadDetail.as_view(), name='imageboard_thread_page'),
    path('<slug:board>/create/', ThreadCreate.as_view(), name='imageboard_thread_create'),
    path('<slug:board>/catalog/', ThreadCatalog.as_view(), name='imageboard_thread_catalog'),  
    path('<slug:board>/', ThreadList.as_view(), name='imageboard_thread_list'), 
]
