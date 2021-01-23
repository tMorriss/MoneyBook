from django.contrib.auth.views import LogoutView
from django.urls import path

from moneybook.views import (AddIntraMoveView, AddView, CheckedDataView,
                             CheckView, CustomLoginView, DeleteView, EditView,
                             indexView, searchView, statisticsView, toolsView)

app_name = 'moneybook'
urlpatterns = [
    path('', indexView.index, name='index'),
    path('<int:year>/<int:month>', indexView.index_month, name='index_month'),
    path('_balance_statisticMini', indexView.index_balance_statistic_mini,
         name='balance_statisticMini'),
    path('_chart_container_data', indexView.index_chart_data,
         name='chart_container_data'),
    path('_data_table', indexView.data_table, name='data_table'),
    path('add', AddView.as_view(), name='add'),
    path('add/intra-move', AddIntraMoveView.as_view(), name='add_intra_move'),
    path('statistics', statisticsView.statistics, name='statistics'),
    path('statistics/<int:year>', statisticsView.statistics_month,
         name='statistics_month'),
    path('search', searchView.search, name='search'),
    path('tools', toolsView.tools, name='tools'),
    path('tools/update-actual-cash',
         toolsView.update_actual_cash, name="update_actual_cash"),
    path('tools/checked_date', CheckedDataView.as_view(), name="checked_date"),
    path('tools/get_several_checked_date',
         toolsView.get_several_checked_date, name="several_checked_date"),
    path('tools/update_credit_checked_date',
         toolsView.update_credit_checked_date,
         name="update_credit_checked_date"),
    path('tools/update_living_cost_mark',
         toolsView.update_living_cost_mark, name="update_living_cost_mark"),
    path('tools/update_now_bank', toolsView.update_now_bank,
         name="update_now_bank"),
    path('tools/unchecked_transaction',
         toolsView.get_unchecked_transaction, name="unchecked_transaction"),
    path('edit/<int:pk>', EditView.as_view(), name='edit'),
    path('edit/check', CheckView.as_view(), name="edit_check"),
    path('delete', DeleteView.as_view(), name='delete'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
