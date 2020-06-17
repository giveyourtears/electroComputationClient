from django.urls import path
from . import views
from light.views import get_render_uo
from accounts.views import get_fes_dic, get_ps_dic

urlpatterns = [
    path('', views.accounting_view, name="accounting"),
    path('select_data/', views.get_render_select_data, name="select_data"),
    path('get_fes/', get_fes_dic, name="get_fes"),
    path('get_ps/', get_ps_dic, name="get_ps")
]
