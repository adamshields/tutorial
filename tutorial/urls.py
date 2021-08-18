from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from django.conf import settings
from snippets.views import SnippetViewSet, UserViewSet
from django.shortcuts import render, Http404, HttpResponseRedirect, get_object_or_404
from servers.views import SoftwareViewSet, ServerViewSet, ServerSoftwareAPIView, ServerListAPIView, TestPage, iommi_view, my_server_detail, my_server_list
# Server2ViewSet # , ServerList, ServerDetail
# from iommi import Table, Form
from servers.models import Server, Software
# from servers.views import TestPage
import debug_toolbar

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
    path('__debug__/', include(debug_toolbar.urls)),
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

# from django.shortcuts import render, Http404, HttpResponseRedirect, get_object_or_404
# # ----------------------------------------------------------------------------------------------------
# # Tables ----------------------------------------------------

# class ServersTableIndexView(Table): # This is manually defined table with specific chosen rows
#     name = Column()
#     status = Column()
#     ip_address = Column()
#     fqdn = Column()
#     software = Column()

# # Views ----------------------------------------------------

# def index(request):
#     return render(
#         request,
#         template_name='index.html',
#         context=dict(
#             content=ServersTableIndexView(rows=Server.objects.all()).bind(request=request), # Calling ServersTableIndexView using the .bind
#             title='Main Page for views using function and html pages'
#         )
#     )
# # ----------------------------------------------------------------------------------------------------


# # ----------------------------------------------------------------------------------------------------
# # Tables ----------------------------------------------------

# class ServersTableUseModel(Table): # Same table type
#     name = Column()
#     status = Column()
#     ip_address = Column()
#     fqdn = Column()

# # Views ----------------------------------------------------

# def index2(request): # using a queryset for return also using this makes it so you don't use the index.html and base.html templates
#     return ServersTableUseModel(
#         title='Servers',
#         rows=Server.objects.all(),
#     )
# # ----------------------------------------------------------------------------------------------------
# urlpatterns += [
#     path('index/', index),
#     path('index2/', index2),
# ]


# # ----------------------------------------------------------------------------------------------------
# # Tables ----------------------------------------------------

# class ServersTableUsingMeta(Table): # using meta values and passing it as_view()
#     name = Column()
#     status = Column()
#     ip_address = Column()
#     fqdn = Column()

#     class Meta:
#         title = 'Servers using meta'
#         rows = Server.objects.all()



# # Views/URLS ----------------------------------------------------
# urlpatterns += [
#     path('index3/', Table(auto__model=Server).as_view()),

# ]

# # ----------------------------------------------------------------------------------------------------
# # Pages ----------------------------------------------------
from iommi.fragment import Fragment
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import (
    login,
    logout,
)
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import Template
from django.urls import (
    path,
    include,
)

class MotherShipMenu(Menu):
    home = MenuItem(url='/', display_name=('Home'))
    servers = MenuItem(display_name=('Servers'))
    software = MenuItem(display_name=('Software'))
    # versions = MenuItem(display_name=_('Versions'))

    class Meta:
        attrs__class = {'fixed-top': True}

class BasePage(Page):
    menu = MotherShipMenu()
    title = html.h1('My awesome webpage')
    subtitle = html.h2('It rocks')

class ServerTable(Table):
    class Meta:
        auto__model = Server
        columns__name__cell__url = lambda row, **_: row.get_absolute_url()
        columns__name__filter__include = True


def index(request):
    class IndexPage(BasePage):
        title = html.img(attrs=dict(src='...', alt='...'))
        # other = html.(attrs=dict(src='...', alt='...'))
        # Fragment('some text', tag='h3')
        # Table(
        #     auto__model=Server,
        #     columns__square=Column(
        #         attr='name',
        #         cell__format=lambda value, **_: value * value,
        #     )
        # )
        server = ServerTable(
            auto__model=Server,
            tag='div',
            header__template=None,
            cell__tag=None,
            row__template=Template("""
                <li> {{ cells.name }}</li>
            """),
        )

        Column(
            cell__url='http://example.com',
            cell__url_title='go to example',
        )

        #     row__template=Template("""
        #         <div class="card" style="width: 15rem; display: inline-block;" {{ cells.attrs }}>
        #             <img class="card-img-top" src="{{ row.server }}/{{ row.name|urlencode }}.jpg">
        #             <div class="card-body text-center">
        #                 <h5>{{ cells.name }}</h5>
        #                 <p class="card-text">
        #                     {{ cells.server }}
        #                 </p>
        #             </div>
        #         </div>
        #     """),
        # )

    return IndexPage()



# # Views/URLS ----------------------------------------------------
urlpatterns += [
    path('yep/', index),
    # path('yep/<slug>/', index),

]

class SoftwareTable(Table):
    class Meta:
        auto__model = Software
        columns__name__cell__url = lambda row, **_: row.get_absolute_url()
        columns__name__filter__include = True


class IndexPageHome(Page):
    menu = MotherShipMenu()
    title = html.h1('MotherShip MerLink View')
    welcome_text = 'This is the index page for Servers multi components'

    servers = Table(auto__model=Server, page_size=5)
    Software = Table(auto__model=Software, page_size=5)

def server_page(request, server):
    # artist = get_object_or_404(Artist, name=artist)
    server = get_object_or_404(Server, name=server)
    # slug = get_object_or_404(Server, name=server)

    class ServerPage(Page):
        menu = MotherShipMenu()
        title = html.h1(server.name)
        

        software = SoftwareTable(auto__rows=Software.objects.filter(server=server))
        # tracks = TrackTable(auto__rows=Track.objects.filter(album__artist=artist))

    return ServerPage()

#         auto__model = Software
#         page_size = 20
#         columns__name__cell__url = lambda row, **_: row.get_absolute_url()
#         columns__name__filter__include = True
#         columns__year__filter__include = True
#         columns__year__filter__field__include = False
#         columns__server__filter__include = True

def software_page(request, software):
    
    software = get_object_or_404(Software, name=software)


    class SoftwarePage(Page):
        menu = MotherShipMenu()
        title = html.h1(software)
        # text = html.a(software.server, attrs__href=software.server.get_absolute_url())

        # tracks = TrackTable(
        #     auto__rows=Track.objects.filter(album=album),
        #     columns__album__include=False,
        # )

    return SoftwarePage()

# # Views/URLS ----------------------------------------------------
urlpatterns += [
    path('', IndexPageHome().as_view()),
    path('servers/', Table(auto__model=Server).as_view()),
    path('servers/<server>/', server_page),
    path('software/', Table(auto__model=Software).as_view()),
    path('software/<software>/', software_page),
    # path('artist/<artist>/<album>/', album_page),

]
# # ----------------------------------------------------------------------------------------------------
# # Pages ----------------------------------------------------

# # # ----------------------------------------------------------------------------------------------------
# # # merlink Pages ----------------------------------------------------


# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib.auth import (
#     login,
#     logout,
# )
# from django.contrib.auth.models import User
# from django.http import HttpResponseRedirect
# from django.shortcuts import get_object_or_404
# from django.template import Template
# from django.urls import (
#     path,
#     include,
# )
# from django.utils.translation import gettext as _

# # import debug_toolbar

# from iommi import (
#     Action,
#     Column,
#     Form,
#     Page,
#     Table,
#     html,
#     Menu,
#     MenuItem,
# )
# from iommi.admin import Admin

# # from .example_data import setup_example_data
# from merlink.models import (
#     Software,
#     Server,
#     Version,
# )

# # setup_example_data()


# # Menu -----------------------------

# class SupernautMenu(Menu):
#     home = MenuItem(url='/', display_name=_('Home'))
#     servers = MenuItem(display_name=_('Servers'))
#     software = MenuItem(display_name=_('Software'))
#     versions = MenuItem(display_name=_('Versions'))

#     class Meta:
#         attrs__class = {'fixed-top': True}


# # Tables ---------------------------

# class VersionTable(Table):
#     class Meta:
#         auto__rows = Version.objects.all()#.select_related('software__server')
#         columns__name__filter__include = True


# class SoftwareTable(Table):
#     class Meta:
#         auto__model = Software
#         page_size = 20
#         columns__name__cell__url = lambda row, **_: row.get_absolute_url()
#         columns__name__filter__include = True
#         columns__year__filter__include = True
#         columns__year__filter__field__include = False
#         columns__server__filter__include = True
#         columns__edit = Column.edit(
#             include=lambda request, **_: request.user.is_staff,
#         )
#         columns__delete = Column.delete(
#             include=lambda request, **_: request.user.is_staff,
#         )
#         actions__create_software = Action(attrs__href='/software/create/', display_name=_('Create software'))


# class ServerTable(Table):
#     class Meta:
#         auto__model = Server
#         columns__name__cell__url = lambda row, **_: row.get_absolute_url()
#         columns__name__filter__include = True


# # Pages ----------------------------


# class IndexPage(Page):
#     menu = SupernautMenu()

#     title = html.h1(_('Supernaut'))
#     welcome_text = html.div(_('This is a discography of the best acts in music!'))

#     log_in = html.a(
#         _('Log in'),
#         attrs__href='/log_in/',
#         include=lambda request, **_: not request.user.is_authenticated,
#     )

#     log_out = html.a(
#         _('Log out'),
#         attrs__href='/log_out/',
#         include=lambda request, **_: request.user.is_authenticated,
#     )

#     software = SoftwareTable(
#         auto__model=Software,
#         tag='div',
#         header__template=None,
#         cell__tag=None,
#         row__template=Template("""
#             <div class="card" style="width: 15rem; display: inline-block;" {{ cells.attrs }}>
#                 <img class="card-img-top" src="/static/software_art/{{ row.server }}/{{ row.name|urlencode }}.jpg">
#                 <div class="card-body text-center">
#                     <h5>{{ cells.name }}</h5>
#                     <p class="card-text">
#                         {{ cells.server }}
#                     </p>
#                 </div>
#             </div>
#         """),
#     )


# def server_page(request, server):
#     server = get_object_or_404(Server, name=server)

#     class ServerPage(Page):
#         title = html.h1(server.name)

#         software = SoftwareTable(auto__rows=Software.objects.filter(server=server))
#         versions = VersionTable(auto__rows=Version.objects.filter(software__server=server))

#     return ServerPage()


# def software_page(request, server, software):
#     software = get_object_or_404(Software, name=software, server__name=server)

#     class SoftwarePage(Page):
#         title = html.h1(software)
#         text = html.a(software.server, attrs__href=software.server.get_absolute_url())

#         versions = VersionTable(
#             auto__rows=Version.objects.filter(software=software),
#             columns__software__include=False,
#         )

#     return SoftwarePage()


# def edit_software(request, server, software):
#     software = get_object_or_404(Software, name=software, server__name=server)
#     return Form.edit(auto__instance=software)


# def delete_software(request, server, software):
#     software = get_object_or_404(Software, name=software, server__name=server)
#     return Form.delete(auto__instance=software)


# def log_in(request):
#     login(request, User.objects.get())
#     return HttpResponseRedirect('/')


# def log_out(request):
#     logout(request)
#     return HttpResponseRedirect('/')


# # URLs -----------------------------
# # class Meta:
# #     apps__Supernaut_album__include = True
# #     apps__Supernaut_artist__include = True
# #     apps__Supernaut_track__include = True

# class MyAdmin(Admin):
#     class Meta:
#         pass


# urlpatterns += [
#     # path('__debug__/', include(debug_toolbar.urls)),

#     path('', IndexPage().as_view()),
#     path('software/', SoftwareTable(auto__model=Software, columns__year__bulk__include=True).as_view()),
#     path('software/create/', Form.create(auto__model=Software).as_view()),
#     path('servers/', ServerTable(auto__model=Server).as_view()),
#     path('versions/', VersionTable(auto__model=Version).as_view()),

#     path('server/<server>/', server_page),
#     path('server/<server>/<software>/', software_page),
#     path('server/<server>/<software>/edit/', edit_software),
#     path('server/<server>/<software>/delete/', delete_software),

#     path('log_in/', log_in),
#     path('log_out/', log_out),

#     path('iommi-admin/', include(MyAdmin.urls())),
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# # # ----------------------------------------------------------------------------------------------------
# # # merlink Pages ----------------------------------------------------
