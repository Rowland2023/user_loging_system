from django.urls import path
from main import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.default, name='default'),
    path('playlist/', views.playlist, name='your_playlists'),
    path('search/', views.search, name='search_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    # Password reset views
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
