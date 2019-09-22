from django.urls import path
from web.views import *

app_name = 'web'
urlpatterns = [
    path('', indexView.index, name='index'),
    path('add', addView.add, name='add'),
    path('statistics', statisticsView.statistics, name='statistics'),
    path('search', searchView.search, name='search'),
    path('tools', toolsView.tools, name='tools'),
    path('edit/<int:pk>', editView.edit, name='edit'),
]