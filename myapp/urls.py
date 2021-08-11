from django.conf.urls import url, include
from rest_framework import routers

import myapp.views as views

router = routers.DefaultRouter()

router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'profile', views.ProfileViewSet, basename='profile')
router.register(r'listing', views.ListingViewSet, basename='listing')
router.register(r'user', views.UserViewSet, basename='user')

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^', include(router.urls)),
]