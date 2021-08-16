from django.urls import path
from servers import views
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
urlpatterns = [
    path('my_servers/', views.my_server_list),
    path('my_servers/<int:pk>/', views.my_server_detail),
    #     path(
    #     'iommi-view-test/{name}',
    #     views.iommi_view
    # ),

]