from django.urls import path, include
from rest_framework import routers
from rest_validator import urls as rest_validator_urls
from api.views import BoardViewListSet, ThreadViewListSet, UserPostViewListSet

router = routers.DefaultRouter()
router.register(r'threads', ThreadViewListSet, base_name='api_thread')
router.register(r'boards', BoardViewListSet, base_name='api_board')
router.register(r'posts', UserPostViewListSet, base_name='api_post')

urlpatterns = [
    path('', include(router.urls)),
    path('captcha/', include(rest_validator_urls)),
] 
