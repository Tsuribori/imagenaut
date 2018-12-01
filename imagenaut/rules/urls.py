from django.urls import path
from .views import RuleList

urlpatterns = [
    path('', RuleList.as_view(), name='rules_rule_list'),
]
