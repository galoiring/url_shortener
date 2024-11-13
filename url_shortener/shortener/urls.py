from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/create/', views.create_url, name='create_url'),
    path('api/urls/', views.get_urls, name='get_urls'),
    path('<str:short_url>/', views.redirect_url, name='redirect_url'),
]
