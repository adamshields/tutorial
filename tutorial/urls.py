from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from snippets.views import SnippetViewSet, UserViewSet
from servers.views import SoftwareViewSet, ServerViewSet, ServerSoftwareAPIView, ServerListAPIView, TestPage, iommi_view, my_server_detail, my_server_list
# Server2ViewSet # , ServerList, ServerDetail
# from iommi import Table, Form
from servers.models import Server, Software
# from servers.views import TestPage

from iommi import (
    Action,
    Column,
    Form,
    Page,
    Table,
    html,
    Menu,
    MenuItem,
)

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
# ...your urls...
# path('iommi-table-test-filter/', Table(
#     auto__model=Server,
#     ip_address__name__filter__include=True,  # <--- replace `name` with some field from your model
# ).as_view()),

urlpatterns = [
    path('fuck/', iommi_view),
    path('admin/', admin.site.urls),
    # path('api/server/', ServerListAPIView.as_view(), name='server_list_api'),
    path('api/server/', server_create_api, name='server_create_api'),
    path('api3/', include(api_router.urls)),
    url(r'^api2/', include('myapp.urls')),
    # path('^adam/', include('servers.urls')),
    path('my_servers/', my_server_list),
    path('my_servers/<int:pk>/', my_server_detail),
    path('iommi-form-test/', Form.create(auto__model=Server).as_view()),
    path('iommi-table-test/', Table(auto__model=Server).as_view()),
    path('iommi-table-test-filter/', Table(
        auto__model=Server,
        # <--- replace `name` with some field from your model
        columns__ip_address__filter__include=True,
    ).as_view()),
    path('iommi-page-test/', TestPage().as_view()),
    

    path('servershit/', include('servers.urls')),
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

from django.shortcuts import render, Http404, HttpResponseRedirect, get_object_or_404
# ----------------------------------------------------------------------------------------------------
# Tables ----------------------------------------------------

class ServersTableIndexView(Table): # This is manually defined table with specific chosen rows
    name = Column()
    status = Column()
    ip_address = Column()
    fqdn = Column()
    software = Column()

# Views ----------------------------------------------------

def index(request):
    return render(
        request,
        template_name='index.html',
        context=dict(
            content=ServersTableIndexView(rows=Server.objects.all()).bind(request=request), # Calling ServersTableIndexView using the .bind
            title='Main Page for views using function and html pages'
        )
    )
# ----------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------
# Tables ----------------------------------------------------

class ServersTableUseModel(Table): # Same table type
    name = Column()
    status = Column()
    ip_address = Column()
    fqdn = Column()

# Views ----------------------------------------------------

def index2(request): # using a queryset for return also using this makes it so you don't use the index.html and base.html templates
    return ServersTableUseModel(
        title='Servers',
        rows=Server.objects.all(),
    )
# ----------------------------------------------------------------------------------------------------
urlpatterns += [
    path('index/', index),
    path('index2/', index2),
]


# ----------------------------------------------------------------------------------------------------
# Tables ----------------------------------------------------

class ServersTableUsingMeta(Table): # using meta values and passing it as_view()
    name = Column()
    status = Column()
    ip_address = Column()
    fqdn = Column()

    class Meta:
        title = 'Servers using meta'
        rows = Server.objects.all()



# Views/URLS ----------------------------------------------------
urlpatterns += [
    path('index3/', Table(auto__model=Server).as_view()),

]

# ----------------------------------------------------------------------------------------------------
# Pages ----------------------------------------------------





class SoftwareTable(Table):
    class Meta:
        auto__model = Software
        columns__name__cell__url = lambda row, **_: row.get_absolute_url()
        columns__name__filter__include = True


class IndexPageHome(Page):
    title = html.h1('MotherShip MerLink View')
    welcome_text = 'This is the index page for Servers multi components'

    servers = Table(auto__model=Server, page_size=5)
    Software = Table(auto__model=Software, page_size=5)

def server_page(request, server):
    # artist = get_object_or_404(Artist, name=artist)
    server = get_object_or_404(Server, name=server)

    class ServerPage(Page):
        title = html.h1(server.name)

        software = SoftwareTable(auto__rows=Software.objects.filter(server=server))
        # tracks = TrackTable(auto__rows=Track.objects.filter(album__artist=artist))

    return ServerPage()



def software_page(request, server, software):
    software = get_object_or_404(Software, name=software, server__name=server)

    class SoftwarePage(Page):
        title = html.h1(software)
        # text = html.a(software.server, attrs__href=software.server.get_absolute_url())

        # tracks = TrackTable(
        #     auto__rows=Track.objects.filter(album=album),
        #     columns__album__include=False,
        # )

    return SoftwarePage()

# Views/URLS ----------------------------------------------------
urlpatterns += [
    path('', IndexPageHome().as_view()),
    path('servers/', Table(auto__model=Server).as_view()),
    path('software/', Table(auto__model=Software).as_view()),
    path('servers/<server>/', server_page),
    path('servers/<software>/', software_page),
    # path('artist/<artist>/<album>/', album_page),

]
# ----------------------------------------------------------------------------------------------------
# Pages ----------------------------------------------------