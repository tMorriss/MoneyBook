function send_add_row() {
    genre = $('input[name="a_genre"]:checked').val();
    direction = 2;
    if (genre == 12) {
        direction = 1;
    }
    $.ajax({
        url: add_url,
        type: "POST",
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "date": $('#a_year').val() + "-" + $('#a_month').val() + "-" + $('#a_day').val(),
            "item": $('#a_item').val(),
            "price": $('#a_price').val(),
            "direction": direction,
            "method": $('input[name="a_method"]:checked').val(),
            "genre": genre,
            "temp": "False",
            "checked": "False",
        }
    })
    // 成功時
    .done(() => {
        if ($('#is-charge').prop('checked')) {
            $.ajax({
                url: add_intra_move_url,
                type: "POST",
                data: {
                    "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
                    "year": $('#a_year').val(),
                    "month": $('#a_month').val(),
                    "day": $('#a_day').val(),
                    "price": $('#a_price').val(),
                    "before_method": 2,
                    "after_method": $('input[name="a_method"]:checked').val(),
                }
            })
            // 成功時
            .done(() => {
                update_success();
            })
            // 失敗時
            .fail(() => {
                // メッセージ表示
                show_result_msg("Error...", empty);
                // 抜ける
                return;
            });
        }
        else {
            update_success();
        }
    })
    // 失敗時
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}
function key_press_add(code) {
    // エンターキーなら実行
    if (code === 13) {
        send_add_row();
    }
}

function move_month() {
    year = document.getElementById("jump_year").value;
    month = document.getElementById("jump_month").value;
    window.location.href = index_url + year + "/" + month;
}
function key_press_move(code) {
    //エンターキーなら
    if (code === 13) {
        move_month();
    }
}

function update_data() {
    $.when(
        $.ajax({
            url: data_table_url,
            type: "GET",
            data: {
                "year": year,
                "month": month,
            }
        })
        .done((data) => {
            $('#transactions').html(data);
            apply_filter();
        }),

        $.ajax({
            url: balance_statisticMini_url,
            type: "GET",
            data: {
                "year": year,
                "month": month,
            }
        })
        .done((data) => {
            $('#statistic-fixed').html(data);
        }),

        $.ajax({
            url: chart_container_data_url,
            type: "GET",
            data: {
                "year": year,
                "month": month,
            }
        })
        .done((data) => {
            $('#js_draw_chart_container').html(data);
        })
    )
    // 成功時
    .done(() => {
        // 円グラフ再描画
        draw_chart_container();
    });
}

function apply_all(elements, status) {
    for (var i = 0; i < elements.length; i++) {
        elements[i].checked = status;
    }
    apply_filter();
}
function select_all() {
    var elements = document.getElementsByClassName('check_filter');
    apply_all(elements, true);
}
function clear_filter() {
    var elements = document.getElementsByName('filter-class[]');
    apply_all(elements, false);
}
function apply_filter() {
    // 各チェックボックスを取得
    var methodList = document.getElementsByName('filter-method[]');
    var classList = document.getElementsByName('filter-class[]');

    // 履歴表のtr
    var rows = document.getElementsByClassName('data-row');
    for (var i = 0; i < rows.length; i++) {
        methodShowing = false;
        // method
        for (var j = 0; j < methodList.length; j++) {
            if (methodList[j].checked && rows[i].classList.contains(methodList[j].id)) {
                methodShowing = true;
                break;
            }
        }
        classShowing = false;
        // class
        for (var j = 0; j < classList.length; j++) {
            if (classList[j].checked && rows[i].classList.contains(classList[j].id)) {
                classShowing = true;
                break;
            }
        }
        if (methodShowing && classShowing) {
            rows[i].classList.remove("hidden-row");
        }
        else {
            rows[i].classList.add("hidden-row");
        }
    }
}

function reset_add_form() {
    // フォームをリセット
    $('#a_day').val('');
    $('#a_item').val('');
    $('#a_price').val('');
    $('input[name=a_method]').val([method_first]);
    $('input[name=a_genre]').val([genre_first]);
    $('#is-charge').prop('checked', false).change();

    // フォーカス
    $('#a_day').focus();
}

function update_success() {
    // データ更新
    update_data();
    // メッセージ表示
    show_result_msg("Success!", reset_add_form);
}
