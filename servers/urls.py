from django.urls import path
from servers import views

urlpatterns = [
    path('my_servers/', views.my_server_list),
    path('my_servers/<int:pk>/', views.my_server_detail),
]