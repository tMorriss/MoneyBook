function separate(num) {
    return String(num).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
}
function unseparate_value(elm) {
    $(elm).val(removeComma($(elm).val()));
}

function separate_value(elm) {
    $(elm).val(separate(Number(removeComma($(elm).val()))));
}

function separate_html(elm) {
    $(elm).html(separate(Number(removeComma($(elm).html()))));
}

function select_value(elm) {
    $(elm).select();
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
    }).done(() => {
        $("#balance_diff").text(value);
        separate_value('#actual_balance')
        separate_html("#balance_diff");
    }).fail(() => {
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
    separate_html("#balance_diff");
}

function get_checked_date() {
    $.get({
        url: checked_date_url,
    }).done((data) => {
        $("#checked-date").html(data);
    })
}

function get_several_checked_date() {
    $.get({
        url: several_checked_date_url,
    }).done((data) => {
        $("#several-checked-date").html(data);
        calculate_now_bank(false);
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
    }).done(() => {
        get_checked_date();
        get_unchecked_transaction();
    }).fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}

function update_several_checked_date(id) {
    $.post({
        url: update_credit_checked_date_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "year": $("#credit_check_year").val(),
            "month": $("#credit_check_month").val(),
            "day": $("#credit_check_day").val(),
            "pk": id,
        }
    }).done(() => {
        // 現在銀行の計算も行う
        calculate_now_bank(true);

        // get_several_checked_date();
    }).fail(() => {
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
    }).done(() => {
        location.reload();
    }).fail(() => {
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
    }).done(() => {
        // チェックした行を削除
        $("#unapproved-row-" + id).remove();
        // 現在銀行も更新
        get_several_checked_date();
    }).fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}

function get_unchecked_transaction() {
    $.get({
        url: unchecked_transaction_url
    }).done((data) => {
        $("#unchecked-transaction").html(data);
    })
}

function calculate_now_bank(isAllUpdate) {
    $(".now_bank_credit").each(function (i, o) {
        if ($(".now_bank_credit").eq(i).val() == "") {
            $(".now_bank_credit").eq(i).val("0");
        }
    })

    // data収集
    data = { "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val() }
    $("[id^=bank-]").each(function () {
        data[$(this).attr("id")] = removeComma($(this).val())
    });
    $("[id^=credit-]").each(function () {
        data[$(this).attr("id")] = removeComma($(this).val())
    });

    $.post({
        url: update_now_bank_url,
        data: data
    }).done((data) => {
        result = JSON.parse(data);
        $("#now_bank_balance").text(separate(result["balance"]));
        document.activeElement.blur();

        if (isAllUpdate) {
            get_several_checked_date();
        }
    }).fail(() => {
        // メッセージ表示
        show_result_msg("Error...", empty);
    });
}
