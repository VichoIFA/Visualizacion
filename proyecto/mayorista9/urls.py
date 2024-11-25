from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Homepage, name='Homepage'),
    path('Login', views.Login, name='Login'),
    path('DashboardInicial/', views.Index,  name='DashboardInicial'),
    path('detalleBarrasAgrupadas/<str:label>/<str:index>', views.BarrasAgrupadas, name='BarrasAgrupadas'),
    path('ComprasCiudad/<str:ciudad>', views.ComprasCiudad, name='ComprasCiudad'),
    path('genero/<str:genero>', views.Genero, name='genero'),
    path('estadoCivil/<str:estadoCivil>', views.estadoCivil, name='estadoCivil'),
    path('DashboardUsuarioCiudad/<str:ciudad>', views.DashboardUsuarioCiudad, name='DashboardUsuarioCiudad'),
    path('profundizacion/<str:ciudad>/<str:producto>', views.Profundizacion, name='profundizacion')
]