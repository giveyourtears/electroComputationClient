from django.contrib import admin
from django.urls import path, include
from substation_info import views

urlpatterns = [
    path('', views.table_view, name="substation_info"),
]
