from django.contrib.auth.views import LogoutView
from django.urls import path
from moneybook.views import (ActualCashView, AddIntraMoveView, AddView,
                             AllInoutMonthView, AllInoutView, CheckedDateView,
                             CheckView, CreditCheckedDateView, CustomLoginView,
                             DataTableView, DeleteView, EditView,
                             IndexBalanceStatisticMiniView, IndexChartDataView,
                             IndexMonthView, IndexView, LivingCostMarkView,
                             NowBankView, PeriodBalanceView, SearchView,
                             SeveralCheckedDateView, StatisticsMonthView,
                             StatisticsView, ToolsView, UncheckedDataView)

app_name = 'moneybook'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:year>/<int:month>', IndexMonthView.as_view(), name='index_month'),
    path('_balance_statistic_mini', IndexBalanceStatisticMiniView.as_view(),
         name='balance_statistic_mini'),
    path('_chart_container_data', IndexChartDataView.as_view(),
         name='chart_container_data'),
    path('_data_table', DataTableView.as_view(), name='data_table'),
    path('add', AddView.as_view(), name='add'),
    path('add/intra-move', AddIntraMoveView.as_view(), name='add_intra_move'),
    path('statistics', StatisticsView.as_view(), name='statistics'),
    path('statistics/<int:year>', StatisticsMonthView.as_view(),
         name='statistics_month'),
    path('all_inout', AllInoutView.as_view(), name='all_inout'),
    path('all_inout/<int:year>', AllInoutMonthView.as_view(), name='all_inout_month'),
    path('period_balances', PeriodBalanceView.as_view(),
         name='period_balances'),
    path('search', SearchView.as_view(), name='search'),
    path('tools', ToolsView.as_view(), name='tools'),
    path('tools/actual_cash',
         ActualCashView.as_view(), name="actual_cash"),
    path('tools/checked_date', CheckedDateView.as_view(), name="checked_date"),
    path('tools/several_checked_date',
         SeveralCheckedDateView.as_view(), name="several_checked_date"),
    path('tools/credit_checked_date',
         CreditCheckedDateView.as_view(),
         name="credit_checked_date"),
    path('tools/living_cost_mark',
         LivingCostMarkView.as_view(), name="living_cost_mark"),
    path('tools/now_bank', NowBankView.as_view(),
         name="now_bank"),
    path('tools/unchecked_transaction',
         UncheckedDataView.as_view(), name="unchecked_transaction"),
    path('edit/<int:pk>', EditView.as_view(), name='edit'),
    path('edit/check', CheckView.as_view(), name="edit_check"),
    path('delete', DeleteView.as_view(), name='delete'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
