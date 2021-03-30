from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('set_csrf', views.set_csrf_token, name="set_csrf")
]
