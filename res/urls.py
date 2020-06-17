from django.urls import path
from . import views

urlpatterns = [
    path('', views.res_view, name="device_info"),
    path('td_data/', views.get_render_table_data, name="td_data"),
]
