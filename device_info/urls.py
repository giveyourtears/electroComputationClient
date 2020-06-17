from django.urls import path
from . import views
from accounts.views import get_fes_dic, get_ps_dic

urlpatterns = [
    path('', views.device_view, name="device_info"),
    path('get_fes/', get_fes_dic, name="get_fes"),
    path('get_ps/', get_ps_dic, name="get_ps"),
    path('archive_day/', views.archive_day_view, name="archive_day"),
    path('archive_month/', views.archive_month_view, name="archive_month"),
    path('rashod_day/', views.rashod_day_view, name="rashod_day"),
    path('rashod_month/', views.rashod_month_view, name="rashod_month"),
]
