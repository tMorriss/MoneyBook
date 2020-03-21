function send_update_row() {
    $.post({
        url: edit_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "date": $('#year').val() + "-" + $('#month').val() + "-" + $('#day').val(),
            "item": $('#item').val(),
            "price": remoteComma($('#price').val()),
            "direction": $('input[name="direction"]:checked').val(),
            "method": $('input[name="method"]:checked').val(),
            "genre": $('input[name="genre"]:checked').val(),
            "temp": $('input[name="temp"]:checked').val(),
            "checked": $('input[name="checked"]:checked').val(),
        }
    })
    // 成功時
    .done(() => {
        window.location.href = document.referrer;
    })
    // 失敗時
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}
function key_press_update(code) {
    // エンターキーなら
    if (code === 13) {
        send_update_row();
    }
}

function send_delete_row() {
    $.post({
        url: delete_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "pk": data_pk,
        }
    })
    // 成功時
    .done(() => {
        window.location.href = document.referrer;
    })
    // 失敗時
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });   
}