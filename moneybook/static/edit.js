function sendUpdateRow() {
    $.post({
        url: edit_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "date": $('#year').val() + "-" + $('#month').val() + "-" + $('#day').val(),
            "item": $('#item').val(),
            "price": removeComma($('#price').val()),
            "direction": $('input[name="direction"]:checked').val(),
            "method": $('input[name="method"]:checked').val(),
            "category": $('input[name="category"]:checked').val(),
            "temp": $('input[name="temp"]:checked').val(),
            "checked": $('input[name="checked"]:checked').val(),
        }
    }).done(() => {
        window.location.href = document.referrer;
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}
function keyPressUpdate(code) {
    // エンターキーなら
    if (code === 13) {
        sendUpdateRow();
    }
}

function sendDeleteRow() {
    $.post({
        url: delete_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "pk": data_pk,
        }
    }).done(() => {
        window.location.href = document.referrer;
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}
