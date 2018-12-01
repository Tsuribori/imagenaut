from django.urls import path
from django.views.generic import TemplateView
from .views import ThreadArchive, ThreadYearArchive, ThreadMonthArchive, ThreadDayArchive, ArchiveSearch

urlpatterns = [
    path('<slug:board>/', ThreadArchive.as_view(), name='archive_thread_list'),  
    path('<slug:board>/<int:year>/', ThreadYearArchive.as_view(), name='archive_thread_year_list'),
    path('<slug:board>/<int:year>/<int:month>/', ThreadMonthArchive.as_view(month_format='%m'), name='archive_thread_month_list'),
    path('<slug:board>/<int:year>/<int:month>/<int:day>/', ThreadDayArchive.as_view(month_format='%m'), name='archive_thread_day_list'),
    path('', ArchiveSearch.as_view(), name='archive_search_form'),
]
