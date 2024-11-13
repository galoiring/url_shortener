from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_short_url, name='create_short_url'),
    path('s/<str:short_code>', views.redirect_to_original,
         name='redirect_to_original'),
]
