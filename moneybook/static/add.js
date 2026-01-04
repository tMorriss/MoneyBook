function sendAddRow() {
    $.post({
        url: add_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "date": $('#a_year').val() + "-" + $('#a_month').val() + "-" + $('#a_day').val(),
            "item": $('#a_item').val(),
            "price": removeComma($('#a_price').val()),
            "direction": $('input[name="a_direction"]:checked').val(),
            "method": $('input[name="a_method"]:checked').val(),
            "category": $('input[name="a_category"]:checked').val(),
            "temp": $('input[name="a_temp"]:checked').val(),
            "checked": "False",
        }
    }).done(() => {
        resetAddForm();
        showResultMsg("Success!", empty);
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

function sendIntraMove() {
    $.post({
        url: intra_move_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "year": $('#m_year').val(),
            "month": $('#m_month').val(),
            "day": $('#m_day').val(),
            "item": $("#m_item").val(),
            "price": removeComma($('#m_price').val()),
            "before_method": $('input[name="m_before_method"]:checked').val(),
            "after_method": $('input[name="m_after_method"]:checked').val(),
        }
    }).done(() => {
        resetAddForm();
        showResultMsg("Success!", empty);
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}
function keyPressIntra(code) {
    // エンターキーなら実行
    if (code === 13) {
        sendIntraMove();
    }
}

function sendCharge() {
    method_id = $('input[name="c_method"]:checked').attr('id');
    label_id = $('#lbl_' + method_id).text();

    $.post({
        url: intra_move_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "year": $('#c_year').val(),
            "month": $('#c_month').val(),
            "day": $('#c_day').val(),
            "item": label_id + "チャージ",
            "price": removeComma($('#c_price').val()),
            "before_method": 2,
            "after_method": $('input[name="c_method"]:checked').val(),
        }
    }).done(() => {
        resetForCharge();
        showResultMsg("Success!", empty);
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}
function keyPressCharge(code) {
    // エンターキーなら実行
    if (code === 13) {
        sendCharge();
    }
}

function sendSuicaCharge() {
    yearValue = $('#s_year').val();
    monthValue = $('#s_month').val();
    dayValue = $('#s_day').val();
    priceValue = $('#s_price').val();
    now = new Date();
    day = (yearValue == now.getFullYear() && monthValue == (now.getMonth() + 1) && dayValue.length == 0) ? now.getDate() : dayValue;
    price = (priceValue.length == 0) ? 5000 : removeComma(priceValue);
    $.post({
        url: add_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "date": `${yearValue}-${monthValue}-${day}`,
            "item": "Suicaチャージ",
            "price": price,
            "direction": 2,
            "method": bank_pk,
            "category": traffic_cost_pk,
            "temp": "False",
            "checked": "False",
        }
    }).done(() => {
        resetForShortcut();
        showResultMsg("Success!", empty);
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}

function resetAddForm() {
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
    $('input[name=a_direction]').val([direction_first]);
    $('input[name=a_method]').val([method_first]);
    $('input[name=a_category]').val([category_first]);
    $('input[name=a_temp]').val(["False"]);
}

function resetForCharge() {
    resetAddForm();

    // チャージの日付にフォーカス
    $('#c_day').focus();
}
function resetForShortcut() {
    resetAddForm();

    // ショートカットの日付にフォーカス
    $('#s_day').focus();
}
