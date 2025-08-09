app_name = 'main'  # 👈 This line registers the 'main' namespace

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('playlist/', views.playlist, name='playlist'),
    path('search/', views.search, name='search'),
]
