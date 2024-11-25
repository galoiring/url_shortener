from django.urls import path
from . import views

app_name = 'shortener'

urlpatterns = [
    path('', views.home, name='home'),
    path('create', views.create_short_url, name='create_short_url'),
    path('s/<str:short_code>', views.redirect_to_original, name='redirect'),
]
