function separate(num){
    return String(num).replace( /(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
}
function unseparate(num) {
    return num.replace(",", "");
}
function unseparate_value(id) {
    var elm = document.getElementById(id);
    elm.value = unseparate(elm.value);
}

function separate_value(id) {
    var elm = document.getElementById(id);
    elm.value = separate(Number(unseparate(elm.value)));
}

function separate_html(id) {
    var elm = document.getElementById(id);
    elm.innerHTML = separate(Number(unseparate(elm.innerHTML)));
}

function delete_value(id) {
    var elm = document.getElementById(id);
    elm.value = "";
}

function update_diff() {
    var written = Number($("#written_balance").text().replace(",", ""));
    var actual = Number($("#actual_balance").val().replace(",", ""));

    var value = written - actual;
    $.ajax({
        url: update_actual_cash_url,
        type: "POST",
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "price": actual,
        }
    })
    // 成功時
    .done(() => {
        $("#balance_diff").text(value);
        separate_value('actual_balance')
        separate_html("balance_diff");
    })
    // 失敗時
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}
function key_press_diff(code) {
    // エンターキーなら
    if (code === 13) {
        update_diff();
    }
}

function show_diff() {
    var written = Number($("#written_balance").text().replace(",", ""));
    var actual = Number($("#actual_balance").val().replace(",", ""));

    var value = written - actual;
    $("#balance_diff").text(value);
    separate_html("balance_diff");
}

function update_checked_date(method_id, checkAll) {
    $.ajax({
        url: update_checked_date_url,
        type: "POST",
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "year": $("#check_year").val(),
            "month": $("#check_month").val(),
            "day": $("#check_day").val(),
            "method": method_id,
            "check_all": checkAll,
        }
    })
    .done(() => {
        location.reload();
    })
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}

function update_several_checked_date(id, url) {
    $.ajax({
        url: url,
        type: "POST",
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "year": $("#credit_check_year").val(),
            "month": $("#credit_check_month").val(),
            "day": $("#credit_check_day").val(),
            "pk": id,
        }
    })
    .done(() => {
        location.reload();
    })
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}

function update_fixed_cost_mark() {
    $.ajax({ 
        url: update_fixed_cost_mark_url,
        type: "POST",
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "price": Number($("#txt_fixed_cost").val().replace(",", "")),
        }
    })
    .done(() => {
        location.reload();
    })
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}
function key_press_fixed(code) {
    // エンターキーなら
    if (code === 13) {
        update_fixed_cost_mark();
    }
}

function check(id) {
    $.ajax({
        url: edit_check_url,
        type: "POST",
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "id": id,
        }
    })
    .done(() => {
        // チェックした行を削除
        $("#unapproved-row-" + id).remove();
    })
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}
