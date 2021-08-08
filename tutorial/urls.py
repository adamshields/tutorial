from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets.views import SnippetViewSet, UserViewSet
from servers.views import SoftwareViewSet, ServerViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', SnippetViewSet)
router.register(r'users', UserViewSet)
router.register(r'software', SoftwareViewSet)
router.register(r'servers', ServerViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]


# from django.urls import include, path
# from rest_framework import routers
# from tutorial.quickstart import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('', include(router.urls)),
#     path('', include('snippets.urls')),  

# ]
# urlpatterns += [
#     path('api-auth/', include('rest_framework.urls')),
# ]

