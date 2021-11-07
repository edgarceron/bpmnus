"""Contains the urls for the form_creator app"""
from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add_user, name='add_user'),
    path('replace/<int:user_id>', views.replace_user, name='replace_user'),
    path('get/<int:user_id>', views.get_user, name='get_user_manticore'),
    path('delete/<int:user_id>', views.delete_user, name='delete_user'),
    path('data_list', views.list_user, name='data_list_user'),
    path('get_user_from_token', views.get_user_from_token, name='get_user_from_token'),
]
