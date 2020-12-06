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
        showResultMsg("Success!", resetAddForm);
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
        showResultMsg("Success!", resetAddForm);
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
    $.post({
        url: intra_move_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "year": $('#c_year').val(),
            "month": $('#c_month').val(),
            "day": $('#c_day').val(),
            "price": removeComma($('#c_price').val()),
            "before_method": 2,
            "after_method": $('input[name="c_method"]:checked').val(),
        }
    }).done(() => {
        showResultMsg("Success!", resetAddForm);
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
    $.post({
        url: add_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "date": $('#s_year').val() + "-" + $('#s_month').val() + "-" + $('#s_day').val(),
            "item": "Suicaチャージ",
            "price": removeComma($('#s_price').val()),
            "direction": 2,
            "method": 2,
            "category": 4,
            "temp": "False",
            "checked": "False",
        }
    }).done(() => {
        showResultMsg("Success!", resetForShortcut);
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}

function sendPayPayCachebackBonus() {
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
        $.post({
            url: add_url,
            data: {
                "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
                "date": $('#s_year').val() + "-" + $('#s_month').val() + "-" + $('#s_day').val(),
                "item": "ボーナス運用",
                "price": removeComma($('#s_price').val()),
                "direction": 2,
                "method": 5,
                "category": 11,
                "temp": "False",
                "checked": "False",
            }
        }).done(() => {
            showResultMsg("Success!", resetForShortcut);
        }).fail(() => {
            // メッセージ表示
            showResultMsg("Error...", empty);
        });
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

function resetForShortcut() {
    resetAddForm();

    // ショートカットの日付にフォーカス
    $('#s_day').focus();
}
