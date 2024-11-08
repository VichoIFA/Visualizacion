from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('DashboardInicial/', views.Index,  name='DashboardInicial'),
    path('detalleBarrasAgrupadas/<str:label>/<str:index>', views.BarrasAgrupadas, name='BarrasAgrupadas'),
    path('Login', views.Login, name='Login'),
    path('', views.Homepage, name='Homepage'),
]