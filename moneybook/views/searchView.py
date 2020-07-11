from django.conf import settings
from django.shortcuts import render
from moneybook.models import Direction, Method, Genre, Data
from datetime import date


def search(request):
    content = {
        'app_name': settings.APP_NAME,
        'username': request.user,
        'directions': Direction.list(),
        'methods': Method.list(),
        'unused_methods': Method.unUsedList(),
        'first_genres': Genre.first_list(),
        'latter_genres': Genre.latter_list(),
        'temps': {0: "No", 1: "Yes"},
        'checkeds': {0: "No", 1: "Yes"},
    }

    # 入力値を維持するための変数
    query_content = {}
    query_list = ["start_year", "start_month", "start_day", "end_year",
                  "end_month", "end_day", "item", "lower_price", "upper_price"]
    for q in query_list:
        if q in request.GET:
            query_content[q] = request.GET.get(q)
    content.update(query_content)

    query_content = {}
    query_list = ["direction", "method", "genre", "temp", "checked"]
    for q in query_list:
        if q in request.GET:
            query_content[q] = list(map(int, request.GET.getlist(q)))
    content.update(query_content)

    # 条件に沿うデータを検索
    if "is_query" in request.GET:
        # 日付
        start_date = None
        if "start_year" in request.GET and "start_month" in request.GET \
                and "start_day" in request.GET:
            if request.GET.get("start_year") != "" \
                    and request.GET.get("start_month") != "" \
                    and request.GET.get("start_day") != "":
                try:
                    date(int(request.GET.get("start_year")),
                         int(request.GET.get("start_month")),
                         int(request.GET.get("start_day")))
                    start_date = request.GET.get(
                        "start_year") + "-" + request.GET.get("start_month") \
                        + "-" + request.GET.get("start_day")
                except:
                    start_date = None
        end_date = None
        if "end_year" in request.GET and "end_month" in request.GET \
                and "end_day" in request.GET:
            if request.GET.get("end_year") != "" \
                and request.GET.get("end_month") != "" \
                    and request.GET.get("end_day") != "":
                try:
                    date(int(request.GET.get("end_year")),
                         int(request.GET.get("end_month")),
                         int(request.GET.get("end_day")))
                    end_date = request.GET.get("end_year") \
                        + "-" + request.GET.get("end_month") \
                        + "-" + request.GET.get("end_day")
                except:
                    end_date = None
        data = Data.getRangeData(start_date, end_date)

        # 品目
        if "item" in request.GET:
            item = request.GET.get("item")
            if item != "":
                data = Data.getKeywordData(data, item)

        # 金額
        if "lower_price" in request.GET \
                and request.GET.get("lower_price") != "":
            try:
                data = Data.filterPrice(
                    data, int(request.GET.get("lower_price")), None
                )
            except:
                data = data
        if "upper_price" in request.GET \
                and request.GET.get("upper_price") != "":
            try:
                data = Data.filterPrice(data, None, int(
                    request.GET.get("upper_price"))
                )
            except:
                data = data

        # 方向
        if "direction" in request.GET:
            try:
                data = Data.filterDirections(data, content["direction"])
            except:
                data = data
        # 支払い方法
        if "method" in request.GET:
            try:
                data = Data.filterMethods(data, content["method"])
            except:
                data = data
        # 分類
        if "genre" in request.GET:
            try:
                data = Data.filterGenres(data, content["genre"])
            except:
                data = data
        # 立替
        if "temp" in request.GET:
            try:
                data = Data.filterTemps(data, content["temp"])
            except:
                data = data
        # チェック済み
        if "checked" in request.GET:
            try:
                data = Data.filterCheckeds(data, content["checked"])
            except:
                data = data

        # 日付順にソート
        data = Data.sortDateAscending(data)

        content.update({
            "show_data": data,
            "income_sum": Data.getIncomeSum(data),
            "outgo_sum": Data.getOutgoSum(data),
            "is_show": True,
        })
    else:
        content.update({"is_show": False})

    return render(request, 'search.html', content)
