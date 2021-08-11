from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from snippets.views import SnippetViewSet, UserViewSet
from servers.views import SoftwareViewSet, ServerViewSet, ServerSoftwareAPIView, ServerListAPIView
#Server2ViewSet # , ServerList, ServerDetail

# Create a router and register our viewsets with it.
api_router = DefaultRouter()
api_router.register(r'snippets', SnippetViewSet)
api_router.register(r'users', UserViewSet)
api_router.register(r'software', SoftwareViewSet)
api_router.register(r'servers', ServerViewSet)
# api_router.register(r'server2', Server2ViewSet, 'server')
server_create_api = ServerSoftwareAPIView.as_view({
    'get': 'list',
    'post': 'create'
})

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/server/', ServerListAPIView.as_view(), name='server_list_api'),
    path('api/server/', server_create_api, name='server_create_api'),
    path('', include(api_router.urls)),
    url(r'^api2/', include('myapp.urls')),
    # path('', include('servers.urls')),
    # path('test/', ServerList.as_view()),
    # path('test/<int:pk>/', ServerDetail.as_view()),
    # path('test/<slug:slug>/', ServerDetail.as_view()),
    # url(r'^v1/', include(api_router.urls, namespace='v1')),
    # url(r'^v1/', include((api_router.urls, 'server'), namespace='v1')),

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

