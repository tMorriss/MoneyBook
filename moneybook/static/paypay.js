function get_transaction() {
    $.ajax({
        url: data_table_url,
        type: "GET",
    })
    .done((data) => {
        $('#transactions').html(data);
    })
}

function send_paypay_cacheback() {
    $.ajax({
        url: add_url,
        type: "POST",
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "date": $('#s_year').val() + "-" + $('#s_month').val() + "-" + $('#s_day').val(),
            "item": "PayPayキャッシュバック",
            "price": $('#s_price').val(),
            "direction": 1,
            "method": 5,
            "genre": 12,
            "temp": "False",
            "checked": "False",
        }
    })
    // 成功時
    .done(() => {
        show_result_msg("Success!", get_transaction);
        reset_form();
    })
    // 失敗時
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}
function key_press_send(code) {
    // エンターキーなら実行
    if (code === 13) {
        send_paypay_cacheback();
    }
}

function reset_form() {
    // フォームをリセット
    $('#s_day').val('');
    $('#s_price').val('');

    // 日付にフォーカス
    $('#s_day').focus();
}