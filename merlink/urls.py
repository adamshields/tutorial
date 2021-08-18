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
from django.utils.translation import gettext as _

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
from iommi.admin import Admin

# from .example_data import setup_example_data
from .models import (
    Software,
    Server,
    Version,
)

# setup_example_data()


# Menu -----------------------------

class SupernautMenu(Menu):
    home = MenuItem(url='/', display_name=_('Home'))
    servers = MenuItem(display_name=_('Servers'))
    software = MenuItem(display_name=_('Software'))
    versions = MenuItem(display_name=_('Versions'))

    class Meta:
        attrs__class = {'fixed-top': True}


# Tables ---------------------------

class VersionTable(Table):
    class Meta:
        auto__rows = Version.objects.all().select_related('software__server')
        columns__name__filter__include = True


class SoftwareTable(Table):
    class Meta:
        auto__model = Software
        page_size = 20
        columns__name__cell__url = lambda row, **_: row.get_absolute_url()
        columns__name__filter__include = True
        columns__year__filter__include = True
        columns__year__filter__field__include = False
        columns__server__filter__include = True
        columns__edit = Column.edit(
            include=lambda request, **_: request.user.is_staff,
        )
        columns__delete = Column.delete(
            include=lambda request, **_: request.user.is_staff,
        )
        actions__create_software = Action(attrs__href='/software/create/', display_name=_('Create software'))


class ArtistTable(Table):
    class Meta:
        auto__model = Server
        columns__name__cell__url = lambda row, **_: row.get_absolute_url()
        columns__name__filter__include = True


# Pages ----------------------------


class IndexPage(Page):
    menu = SupernautMenu()

    title = html.h1(_('Supernaut'))
    welcome_text = html.div(_('This is a discography of the best acts in music!'))

    log_in = html.a(
        _('Log in'),
        attrs__href='/log_in/',
        include=lambda request, **_: not request.user.is_authenticated,
    )

    log_out = html.a(
        _('Log out'),
        attrs__href='/log_out/',
        include=lambda request, **_: request.user.is_authenticated,
    )

    software = SoftwareTable(
        auto__model=Software,
        tag='div',
        header__template=None,
        cell__tag=None,
        row__template=Template("""
            <div class="card" style="width: 15rem; display: inline-block;" {{ cells.attrs }}>
                <img class="card-img-top" src="/static/software_art/{{ row.server }}/{{ row.name|urlencode }}.jpg">
                <div class="card-body text-center">
                    <h5>{{ cells.name }}</h5>
                    <p class="card-text">
                        {{ cells.server }}
                    </p>
                </div>
            </div>
        """),
    )


def server_page(request, server):
    server = get_object_or_404(Server, name=server)

    class ArtistPage(Page):
        title = html.h1(server.name)

        software = SoftwareTable(auto__rows=Software.objects.filter(server=server))
        versions = VersionTable(auto__rows=Version.objects.filter(software__server=server))

    return ArtistPage()


def software_page(request, server, software):
    software = get_object_or_404(Software, name=software, server__name=server)

    class AlbumPage(Page):
        title = html.h1(software)
        text = html.a(software.server, attrs__href=software.server.get_absolute_url())

        versions = VersionTable(
            auto__rows=Version.objects.filter(software=software),
            columns__software__include=False,
        )

    return AlbumPage()


def edit_software(request, server, software):
    software = get_object_or_404(Software, name=software, server__name=server)
    return Form.edit(auto__instance=software)


def delete_software(request, server, software):
    software = get_object_or_404(Software, name=software, server__name=server)
    return Form.delete(auto__instance=software)


def log_in(request):
    login(request, User.objects.get())
    return HttpResponseRedirect('/')


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


# URLs -----------------------------

class MyAdmin(Admin):
    class Meta:
        pass


urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),

    path('', IndexPage().as_view()),
    path('software/', SoftwareTable(auto__model=Software, columns__year__bulk__include=True).as_view()),
    path('software/create/', Form.create(auto__model=Software).as_view()),
    path('servers/', ArtistTable(auto__model=Server).as_view()),
    path('versions/', VersionTable(auto__model=Version).as_view()),

    path('server/<server>/', server_page),
    path('server/<server>/<software>/', software_page),
    path('server/<server>/<software>/edit/', edit_software),
    path('server/<server>/<software>/delete/', delete_software),

    path('log_in/', log_in),
    path('log_out/', log_out),

    path('iommi-admin/', include(MyAdmin.urls())),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
