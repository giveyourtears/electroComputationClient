from django.urls import path
from . import views
from accounts.views import login_view, logout_view

urlpatterns = [
    path('menu/', views.index_view, name="home"),
    path('logout/', logout_view),
    path('', login_view, name="login"),
]
