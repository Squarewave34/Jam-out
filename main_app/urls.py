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

  #dev logs
  path('devLogs/<int:game_jam_id>', views.dev_logs, name='dev-logs'),
  path('devLogs/<int:game_jam_id>/show-dev-log-form/', views.show_dev_log_form, name='show-dev-log-form'),
  path('devLogs/<int:game_jam_id>/add-dev-log/', views.add_dev_log, name='add-dev-log'),
  path('devLogs/<int:game_jam_id>/<int:dev_log_id>/', views.dev_log_details, name='dev-log-details'),
  path('devLogs/<int:pk>/update/', views.DevLogUpdate.as_view(), name='dev-log-update'),
  path('devLogs/<int:pk>/delete/', views.DevLogDelete.as_view(), name='dev-log-delete'),

  path('threads/', views.threads, name='threads'),
  path('threads/create', views.ThreadCreate.as_view(), name='thread-create'),
  path('threads/<int:thread_id>/', views.thread_details, name='thread-details'),
  path('threads/<int:pk>/update/', views.ThreadUpdate.as_view(), name='thread-update'),
  path('threads/<int:pk>/delete/', views.ThreadDelete.as_view(), name='thread-delete'),

  path('users/', views.users, name='users'),

  path('profile/', views.profile, name='profile'),
]