from django.urls import path# type: ignore
from django.contrib.auth import views as auth_views# type: ignore
from . import views
from django.contrib.auth.views import LogoutView# type: ignore

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('room/<int:room_id>/', views.room, name='room'),
    # path('create-room/', views.create_room, name='create_room'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('join-room/<int:room_id>/', views.join_room, name='join_room'),
    path('create-room/', views.create_room, name='create_room'),  # Define the URL for create_room
    path('room/<int:room_id>/', views.room_view, name='room'), 
]