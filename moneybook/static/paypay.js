function getTransaction() {
    $.get({
        url: data_table_url,
    }).done((data) => {
        $('#transactions').html(data);
    })
}

function sendPaypayCacheback() {
    $.post({
        url: add_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "date": $('#s_year').val() + "-" + $('#s_month').val() + "-" + $('#s_day').val(),
            "item": "PayPayキャッシュバック",
            "price": removeComma($('#s_price').val()),
            "direction": 1,
            "method": 5,
            "category": 12,
            "temp": "False",
            "checked": "False",
        }
    }).done(() => {
        showResultMsg("Success!", getTransaction);
        getPaypayBalance();
        resetForm();
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}
function keyPressSend(code) {
    // エンターキーなら実行
    if (code === 13) {
        sendPaypayCacheback();
    }
}

function updateCachebackDate() {
    $.post({
        url: cacheback_checked_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "year": $("#c_year").val(),
            "month": $("#c_month").val(),
            "day": $("#c_day").val(),
            "pk": 1,
        }
    }).done(() => {
        showResultMsg("Success!", getTransaction);
        resetForm();
    });
}
function keyPressCacheback(code) {
    // エンターキーなら実行
    if (code === 13) {
        updateCachebackDate();
    }
}

function getPaypayBalance() {
    $.get({
        url: paypay_balance_url
    }).done((data) => {
        result = JSON.parse(data);
        $("#paypay_balance").text(separate(result["balance"]) + "円");
    });
}

function resetForm() {
    // フォームをリセット
    $('#s_day').val('');
    $('#s_price').val('');

    // 日付にフォーカス
    $('#s_day').focus();
}
