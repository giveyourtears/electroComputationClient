from django.urls import path
from light.views import light_view, get_render_uo
from accounts.views import get_fes_dic

urlpatterns = [
    path('', light_view, name="light"),
    path('get_fes', get_fes_dic, name="get_fes"),
    path('select_uo', get_render_uo, name="get_render_uo"),
]
