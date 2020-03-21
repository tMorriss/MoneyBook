function send_add_row() {
    $.post({
        url: add_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "date": $('#a_year').val() + "-" + $('#a_month').val() + "-" + $('#a_day').val(),
            "item": $('#a_item').val(),
            "price": $('#a_price').val(),
            "direction": $('input[name="a_direction"]:checked').val(),
            "method": $('input[name="a_method"]:checked').val(),
            "genre": $('input[name="a_genre"]:checked').val(),
            "temp": $('input[name="a_temp"]:checked').val(),
            "checked": "False",
        }
    })
    // 成功時
    .done(() => {
        show_result_msg("Success!", reset_add_form);
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

function send_intra_move() {
    $.post({
        url: intra_move_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "year": $('#m_year').val(),
            "month": $('#m_month').val(),
            "day": $('#m_day').val(),
            "item": $("#m_item").val(),
            "price": $('#m_price').val(),
            "before_method": $('input[name="m_before_method"]:checked').val(),
            "after_method": $('input[name="m_after_method"]:checked').val(),
        }
    })
    // 成功時
    .done(() => {
        show_result_msg("Success!", reset_add_form);
    })
    // 失敗時
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}
function key_press_intra(code) {
    // エンターキーなら実行
    if (code === 13) {
        send_intra_move();
    }
}

function send_charge() {
    $.post({
        url: intra_move_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "year": $('#c_year').val(),
            "month": $('#c_month').val(),
            "day": $('#c_day').val(),
            "price": $('#c_price').val(),
            "before_method": 2,
            "after_method": $('input[name="c_method"]:checked').val(),
        }
    })
    // 成功時
    .done(() => {
        show_result_msg("Success!", reset_add_form);
    })
    // 失敗時
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}
function key_press_charge(code) {
    // エンターキーなら実行
    if (code === 13) {
        send_charge();
    }
}

function send_suica_charge() {
    $.post({
        url: add_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "date": $('#s_year').val() + "-" + $('#s_month').val() + "-" + $('#s_day').val(),
            "item": "Suicaチャージ",
            "price": $('#s_price').val(),
            "direction": 2,
            "method": 2,
            "genre": 4,
            "temp": "False",
            "checked": "False",
        }
    })
    // 成功時
    .done(() => {
        show_result_msg("Success!", reset_for_shortcut);
    })
    // 失敗時
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}

function reset_add_form() {
    // フォームをリセット
    // チャージ
    $('#c_day').val('');
    $('#c_item').val('');
    $('#c_price').val('');
    $('input[name=c_method]').val([method_first]);

    // 内部移動
    $('#m_day').val('');
    $('#m_item').val('');
    $('#m_price').val('');
    $('input[name=m_before_method]').val([method_first]);
    $('input[name=m_after_method]').val([method_first]);

    // ショートカット
    $('#s_day').val('');
    $('#s_price').val('');

    // 通常追加
    $('#a_day').val('');
    $('#a_item').val('');
    $('#a_price').val('');
    $('input[name=a_method]').val([method_first]);
    $('input[name=a_genre]').val([genre_first]);
    $('#is-charge').prop('checked', false).change();
}
function reset_for_shortcut() {
    reset_add_form();

    // ショートカットの日付にフォーカス
    $('#s_day').focus();
}