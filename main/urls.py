from django.urls import path
from main import views

urlpatterns = [
    path('', views.default, name='default'),
    path('playlist/', views.playlist, name='your_playlists'),
    path('search/', views.search, name='search_page'),
    path('login/', views.login_view, name='login'),
]
