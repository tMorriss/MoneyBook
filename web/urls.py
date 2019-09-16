from django.urls import path
from . import views

app_name = 'web'
urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('statistics', views.statistics, name='statistics'),
    path('search', views.search, name='search'),
]