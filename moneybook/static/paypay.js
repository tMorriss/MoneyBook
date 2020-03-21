function separate(num){
    return String(num).replace( /(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
}
function get_transaction() {
    $.get({
        url: data_table_url,
    })
    .done((data) => {
        $('#transactions').html(data);
    })
}

function send_paypay_cacheback() {
    $.post({
        url: add_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "date": $('#s_year').val() + "-" + $('#s_month').val() + "-" + $('#s_day').val(),
            "item": "PayPayキャッシュバック",
            "price": removeComma($('#s_price').val()),
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
        get_payapy_balance();
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

function update_cacheback_date() {
    $.post({
        url: cacheback_checked_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "year": $("#c_year").val(),
            "month": $("#c_month").val(),
            "day": $("#c_day").val(),
            "pk": 1,
        }
    })
    .done(() => {
        show_result_msg("Success!", get_transaction);
        reset_form();
    });
}
function key_press_cacheback(code) {
    // エンターキーなら実行
    if (code === 13) {
        update_cacheback_date();
    }
}

function get_payapy_balance() {
    $.get({
        url: paypay_balance_url
    })
    .done((data) => {
        result = JSON.parse(data);
        $("#paypay_balance").text(separate(result["balance"]) + "円");
    });
}

function reset_form() {
    // フォームをリセット
    $('#s_day').val('');
    $('#s_price').val('');

    // 日付にフォーカス
    $('#s_day').focus();
}