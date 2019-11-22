from django.urls import path
from moneybook.views import *
from django.contrib.auth.views import LogoutView

app_name = 'moneybook'
urlpatterns = [
    path('', indexView.index, name='index'),
    path('<int:year>/<int:month>', indexView.index_month, name='index_month'),
    path('add', AddView.as_view(), name='add'),
    path('add/intra-move', AddIntraMoveView.as_view(), name='add_intra_move'),
    path('statistics', statisticsView.statistics, name='statistics'),
    path('statistics/<int:year>', statisticsView.statistics_month, name='statistics_month'),
    path('search', searchView.search, name='search'),
    path('tools', toolsView.tools, name='tools'),
    path('tools/update-actual-cash', toolsView.update_actual_cash, name="update_actual_cash"),
    path('tools/update_checked_date', toolsView.update_checked_date, name="update_checked_date"),
    path('tools/update_credit_checked_date', toolsView.update_credit_checked_date, name="update_credit_checked_date"),
    path('tools/update_cacheback_checked_date', toolsView.update_cacheback_checked_date, name="update_cacheback_checked_date"),
    path('tools/update_fixed_cost_mark', toolsView.update_fixed_cost_mark, name="update_fixed_cost_mark"),
    path('tools/calculate_now_bank', toolsView.calculate_now_bank, name="calculate_now_bank"),
    path('edit/<int:pk>', EditView.as_view(), name='edit'),
    path('edit/check', CheckView.as_view(), name="edit_check"),
    path('delete', DeleteView.as_view(), name='delete'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]