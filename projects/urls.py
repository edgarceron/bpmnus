"""Contains the urls for the form_creator app"""
from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add_project, name='add_project'),
    path('replace/<int:project_id>', views.replace_project, name='replace_project'),
    path('get/<int:project_id>', views.get_project, name='get_project_manticore'),
    path('delete/<int:project_id>', views.delete_project, name='delete_project'),
    path('delete_bulk_project', views.delete_bulk_project, name='delete_bulk_project'),
    path('data_list', views.list_project, name='data_list_project'),
]
