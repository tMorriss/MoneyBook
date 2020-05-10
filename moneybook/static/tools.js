function separate(num){
    return String(num).replace( /(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
}
function unseparate_value(id) {
    var elm = document.getElementById(id);
    elm.value = removeComma(elm.value);
}

function separate_value(id) {
    var elm = document.getElementById(id);
    elm.value = separate(Number(removeComma(elm.value)));
}

function separate_html(id) {
    var elm = document.getElementById(id);
    elm.innerHTML = separate(Number(removeComma(elm.innerHTML)));
}

function delete_value(id) {
    var elm = document.getElementById(id);
    elm.value = "";
}

function update_diff() {
    var written = Number(removeComma($("#written_balance").text()));
    var actual = Number(removeComma($("#actual_balance").val()));

    var value = written - actual;
    $.post({
        url: update_actual_cash_url,
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

function get_checked_date() {
    $.get({
        url: checked_date_url,
    })
    .done((data) => {
        $("#checked-date").html(data);
    })
}

function get_several_checked_date() {
    $.get({
        url: several_checked_date_url,
    })
    .done((data) => {
        $("#several-checked-date").html(data);
        calculate_now_bank();
    })
}

function update_checked_date(method_id, checkAll) {
    $.post({
        url: checked_date_url,
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
        get_checked_date();
        get_unchecked_transaction();
    })
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}

function update_several_checked_date(id, url) {
    $.post({
        url: url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "year": $("#credit_check_year").val(),
            "month": $("#credit_check_month").val(),
            "day": $("#credit_check_day").val(),
            "pk": id,
        }
    })
    .done(() => {
        get_several_checked_date();
    })
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}

function update_fixed_cost_mark() {
    $.post({
        url: update_fixed_cost_mark_url,
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
    $.post({
        url: edit_check_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "id": id,
        }
    })
    .done(() => {
        // チェックした行を削除
        $("#unapproved-row-" + id).remove();
        // 現在銀行も更新
        get_several_checked_date();
    })
    .fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}

function get_unchecked_transaction() {
    $.get({
        url: unchecked_transaction_url
    })
    .done((data) => {
        $("#unchecked-transaction").html(data);
    })
}