function sendAddRow() {
    category = $('input[name="a_category"]:checked').val();
    // カテゴリのデフォルト方向を取得（デフォルトは支出:2）
    direction = category_directions[category] || 2;

    // 立替フラグの値を取得
    const tempValue = $('input[name="a_temp"]:checked').val();
    // 立替の場合、収支を逆転させる
    if (tempValue === 'True') {
        direction = 3 - direction;
    }

    yearValue = $('#a_year').val();
    monthValue = $('#a_month').val();
    dayValue = $('#a_day').val();
    now = new Date();
    day = (yearValue == now.getFullYear() && monthValue == (now.getMonth() + 1) && dayValue.length == 0) ? now.getDate() : dayValue;
    $.post({
        url: add_api_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "date": `${yearValue}-${monthValue}-${day}`,
            "item": $('#a_item').val(),
            "price": evaluateFormula($('#a_price').val()),
            "direction": direction,
            "method": $('input[name="a_method"]:checked').val(),
            "category": category,
            "temp": tempValue,
            "checked": "False",
        }
    }).done(() => {
        updateSuccess();
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
    var count = 0;
    var incomeSum = 0;
    var outgoSum = 0;

    for (var i = 0; i < rows.length; i++) {
        var $row = $(rows[i]);
        // 検索
        wordShowing = true;
        if (keyword.length >= 0 && $row.children('.data_item').html().indexOf(keyword) < 0) {
            wordShowing = false;
        }
        // direction
        directionShowing = false;
        for (var j = 0; j < directionList.length; j++) {
            if (directionList[j].checked && $row.hasClass(directionList[j].id)) {
                directionShowing = true;
                break;
            }
        }
        // method
        methodShowing = false;
        for (var j = 0; j < methodList.length; j++) {
            if (methodList[j].checked && $row.hasClass(methodList[j].id)) {
                methodShowing = true;
                break;
            }
        }
        // class
        classShowing = false;
        for (var j = 0; j < classList.length; j++) {
            if (classList[j].checked && $row.hasClass(classList[j].id)) {
                classShowing = true;
                break;
            }
        }
        if (wordShowing && directionShowing && methodShowing && classShowing) {
            $row.removeClass('hidden-row');

            // 合計計算
            count++;
            var price = parseInt($row.find('.data-price').attr('data-price'), 10);
            if ($row.hasClass('filter-direction-1')) {
                incomeSum += price;
            } else if ($row.hasClass('filter-direction-2')) {
                outgoSum += price;
            }
        }
        else {
            $row.addClass('hidden-row');
        }
    }
    // 集計表示更新
    $('#summary-count').text(count + '件');
    $('#summary-income').text('収入: ' + separate(incomeSum) + '円');
    $('#summary-outgo').text('支出: ' + separate(outgoSum) + '円');
}

function resetAddForm() {
    // フォームをリセット
    $('#a_day').val('');
    $('#a_item').val('');
    $('#a_price').val('');
    $('input[name=a_method]').val([method_first]);
    $('input[name=a_category]').val([category_first]);
    $('input[name=a_temp]').val(["False"]);

    // フォーカス
    $('#a_day').focus();
}

function updateSuccess() {
    resetAddForm();
    // データ更新
    fetchData();
    // メッセージ表示
    showResultMsg("Success!", empty);
}

let root = null;
function drawChartContainer() {
    if (root) {
        root.dispose();
    }

    // データ収集
    const chartDataLi = $("#chart_data li");
    const data = [];
    let dataSum = 0;
    for (var i = 0; i < chartDataLi.length; i++) {
        const item = chartDataLi[i].textContent.split(',');
        const value = Number(item[1]);
        data.push({ category: item[0], value: value });
        dataSum += value;
    }

    // データが無いときは描画しない
    if (dataSum == 0) {
        return;
    }

    root = am5.Root.new("chart_container");

    // テーマ
    root.setThemes([
        am5themes_Animated.new(root),
        am5themes_Kelly.new(root)
    ]);

    var chart = root.container.children.push(
        am5percent.PieChart.new(root, {
            radius: am5.percent(60),
            innerRadius: am5.percent(30)
        })
    );

    // Series設定
    var series = chart.series.push(
        am5percent.PieSeries.new(root, {
            valueField: "value",
            categoryField: "category",
            alignLabels: false
        })
    );

    series.slices.template.setAll({
        strokeWidth: 0,
        tooltipText: "{category}: {value}円 ({valuePercentTotal.formatNumber('#.')}%)"
    });

    series.labels.template.setAll({
        text: "{category}\n{value}円",
        textType: "circular",
        centerX: am5.percent(100)
    });

    series.data.setAll(data);

    // アニメーション
    series.appear(1000, 100);

    var label = chart.seriesContainer.children.push(am5.Label.new(root, {
        text: "支出内訳",
        fontSize: "1.7vw",
        centerX: am5.percent(50),
        centerY: am5.percent(50),
        populateText: true
    }));

    // スマホのとき
    if ($('#is_pc').css("visibility") == 'hidden') {
        label.set("fontSize", "7vw");
    }
}
