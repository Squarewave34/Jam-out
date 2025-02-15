from django.contrib import admin
from django.urls import path
from . import views

#   path('', views., name=''),

urlpatterns = [
  path('', views.home, name='home'),
  path('main/', views.main, name='main'),

  # game jams
  path('gameJams/', views.game_jams, name='game-jams'),
  path('gameJams/<int:game_jam_id>', views.game_jam_details, name='game-jam-details'),
  path('gameJams/create', views.GameJamCreate.as_view(), name='game-jam-create'),
  path('gameJams/<int:pk>/update/', views.GameJamUpdate.as_view(), name='game-jam-update'),
  path('gameJams/<int:pk>/delete/', views.GameJamDelete.as_view(), name='game-jam-delete'),

  # roles
  path('roles/<int:game_jam_id>/', views.allRoles, name='all-roles'),
  path('roles/<int:game_jam_id>/add-role/', views.add_role, name='add-role'),
  path('roles/<int:pk>/update/', views.RoleUpdate.as_view(), name='role-update'),
  path('roles/<int:pk>/delete/', views.RoleDelete.as_view(), name='role-delete'),

  path('threads/', views.threads, name='threads'),

  path('users/', views.users, name='users'),

  path('profile/', views.profile, name='profile'),
]