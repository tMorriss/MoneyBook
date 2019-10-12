from django.urls import path
from web.views import *

app_name = 'web'
urlpatterns = [
    path('', indexView.index, name='index'),
    path('<int:year>/<int:month>', indexView.index_month, name='index_month'),
    path('add', AddView.as_view(), name='add'),
    path('add/intra-move', AddIntraMoveView.as_view(), name='add_intra_move'),
    path('statistics', statisticsView.statistics, name='statistics'),
    path('search', searchView.search, name='search'),
    path('tools', toolsView.tools, name='tools'),
    path('edit/<int:pk>', EditView.as_view(), name='edit'),
    path('delete', DeleteView.as_view(), name='delete')
]