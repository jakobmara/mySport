from django.urls import path

from . import views

app_name = 'mySport'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:player_id>/',views.detail,name='detail'),
    path('search/', views.searchResults, name='searchResults'),
    path('team/<int:team_id>/',views.teamDetail, name='teamDetail')
]
