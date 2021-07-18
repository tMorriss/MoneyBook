function sendAddRow() {
    category = $('input[name="a_category"]:checked').val();
    direction = 2;
    if (category == 12) {
        direction = 1;
    }
    $.post({
        url: add_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "date": $('#a_year').val() + "-" + $('#a_month').val() + "-" + $('#a_day').val(),
            "item": $('#a_item').val(),
            "price": removeComma($('#a_price').val()),
            "direction": direction,
            "method": $('input[name="a_method"]:checked').val(),
            "category": category,
            "temp": "False",
            "checked": "False",
        }
    }).done(() => {
        method_id = $('input[name="a_method"]:checked').attr('id');
        label_id = $('#lbl_' + method_id).text();

        if ($('#is-charge').prop('checked')) {
            $.post({
                url: add_intra_move_url,
                data: {
                    "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
                    "year": $('#a_year').val(),
                    "month": $('#a_month').val(),
                    "day": $('#a_day').val(),
                    "item": label_id + "チャージ",
                    "price": removeComma($('#a_price').val()),
                    "before_method": 2,
                    "after_method": $('input[name="a_method"]:checked').val(),
                }
            }).done(() => {
                updateSuccess();
            }).fail(() => {
                // メッセージ表示
                showResultMsg("Error...", empty);
                // 抜ける
                return;
            });
        }
        else {
            updateSuccess();
        }
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}
function keyPressAdd(code) {
    // エンターキーなら実行
    if (code === 13) {
        sendAddRow();
    }
}

function moveMonth() {
    year = $("#jump_year").val();
    month = $("#jump_month").val();
    window.location.href = index_url + year + "/" + month;
}
function key_press_move(code) {
    //エンターキーなら
    if (code === 13) {
        moveMonth();
    }
}

function fetchData() {
    $.when(
        $.get({
            url: data_table_url,
            data: {
                "year": year,
                "month": month,
            }
        }).done((data) => {
            $('#transactions').html(data);
            applyFilter();
        }),

        $.get({
            url: balance_statistic_mini_url,
            data: {
                "year": year,
                "month": month,
            }
        }).done((data) => {
            $('#statistic-fixed').html(data);
        }),

        $.get({
            url: chart_container_data_url,
            data: {
                "year": year,
                "month": month,
            }
        }).done((data) => {
            $('#chart_container_data').html(data);
        })
    ).done(() => {
        // 円グラフ再描画
        drawChartContainer();
    });
}

function applyAll(elements, status) {
    for (var i = 0; i < elements.length; i++) {
        elements[i].checked = status;
    }
    applyFilter();
}
function selectAll() {
    var elements = $('.check_filter');
    applyAll(elements, true);
}
function clearFilter() {
    var elements = $('[name="filter-class[]"]');
    applyAll(elements, false);
}
function applyFilter() {
    // 検索ワードを取得
    var keyword = $('#filter-item').val();
    // 各チェックボックスを取得
    var directionList = $('[name="filter-direction[]"]');
    var methodList = $('[name="filter-method[]"]');
    var classList = $('[name="filter-class[]"]');

    // 履歴表のtr
    var rows = $('.data-row');
    for (var i = 0; i < rows.length; i++) {
        // 検索
        wordShowing = true;
        if (keyword.length >= 0 && $(rows[i]).children('.data_item').html().indexOf(keyword) < 0) {
            wordShowing = false;
        }
        // direction
        directionShowing = false;
        for (var j = 0; j < directionList.length; j++) {
            if (directionList[j].checked && $(rows[i]).hasClass(directionList[j].id)) {
                directionShowing = true;
                break;
            }
        }
        // method
        methodShowing = false;
        for (var j = 0; j < methodList.length; j++) {
            if (methodList[j].checked && $(rows[i]).hasClass(methodList[j].id)) {
                methodShowing = true;
                break;
            }
        }
        // class
        classShowing = false;
        for (var j = 0; j < classList.length; j++) {
            if (classList[j].checked && $(rows[i]).hasClass(classList[j].id)) {
                classShowing = true;
                break;
            }
        }
        if (wordShowing && directionShowing && methodShowing && classShowing) {
            $(rows[i]).removeClass("hidden-row");
        }
        else {
            $(rows[i]).addClass("hidden-row");
        }
    }
}

function resetAddForm() {
    // フォームをリセット
    $('#a_day').val('');
    $('#a_item').val('');
    $('#a_price').val('');
    $('input[name=a_method]').val([method_first]);
    $('input[name=a_category]').val([category_first]);
    $('#is-charge').prop('checked', false).change();

    // フォーカス
    $('#a_day').focus();
}

function updateSuccess() {
    // データ更新
    fetchData();
    // メッセージ表示
    showResultMsg("Success!", resetAddForm);
}

function drawChartContainer() {
    am4core.ready(function () {
        // テーマ
        am4core.useTheme(am4themes_animated);
        am4core.useTheme(am4themes_kelly);

        var chart = am4core.create("chart_container", am4charts.PieChart);

        // データ収集
        const chartData = $("#chart_data li");
        chart.data = [];
        dataSum = 0;
        for (var i = 0; i < chartData.length; i++) {
            data = chartData[i].textContent.split(',');
            chart.data.push({ category: data[0], value: data[1] });
            dataSum += Number(data[1]);
        }

        // データが無いときは描画しない
        if (dataSum == 0) {
            return;
        }

        chart.radius = am4core.percent(60);
        chart.innerRadius = am4core.percent(30);

        // Series設定
        var pieSeries = chart.series.push(new am4charts.PieSeries());
        pieSeries.dataFields.value = "value";
        pieSeries.dataFields.category = "category";
        pieSeries.slices.template.strokeWidth = 0;
        pieSeries.labels.template.text = "{category}\n{value.value}円";
        pieSeries.slices.template.tooltipText = "{category}: {value.value}円 ({value.percent.formatNumber('#.')}%)";

        // アニメーションの開始設定
        pieSeries.hiddenState.properties.opacity = 1;
        pieSeries.hiddenState.properties.endAngle = -90;
        pieSeries.hiddenState.properties.startAngle = -90;

        var label = pieSeries.createChild(am4core.Label);
        label.text = "支出内訳";
        label.horizontalCenter = "middle";
        label.verticalCenter = "middle";
        label.fontSize = "1.7vw";

        // スマホのとき
        if ($('#is_pc').css("visibility") == 'hidden') {
            label.fontSize = "7vw";
        }
    });
}
