function unseparateValue(elm) {
    $(elm).val(removeComma($(elm).val()));
}

function separateValue(elm) {
    $(elm).val(separate(Number(removeComma($(elm).val()))));
}

function separateHtml(elm) {
    $(elm).html(separate(Number(removeComma($(elm).html()))));
}

function selectValue(elm) {
    $(elm).select();
}

function updateDiff() {
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
        separateValue('#actual_balance')
        separateHtml("#balance_diff");
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}
function KeyPressDiff(code) {
    // エンターキーなら
    if (code === 13) {
        updateDiff();
    }
}

function showDiff() {
    var written = Number($("#written_balance").text().replace(",", ""));
    var actual = Number($("#actual_balance").val().replace(",", ""));

    var value = written - actual;
    $("#balance_diff").text(value);
    separateHtml("#balance_diff");
}

function getCheckedDate() {
    $.get({
        url: checked_date_url,
    }).done((data) => {
        let dataJson = JSON.parse(data);

        // 既存を削除
        $(".checked-date-row").remove();

        // 現在の値を追加
        for (var i = 0; i < dataJson.length; i++) {
            var checkAll = 1;
            if (dataJson[i].pk == 2) {
                checkAll = 0;
            }
            var rowText = '<tr class="checked-date-row">';
            rowText += '<td>';
            rowText += '<input type="button" class="btn-apply" value="' + dataJson[i].name + '" onclick="updateCheckedDate(' + dataJson[i].pk + ', ' + checkAll + ')">'
            rowText += '</td>';
            rowText += '<td>現在: ' + dataJson[i].year + '年' + dataJson[i].month + '月' + dataJson[i].day + '日</td>';
            rowText += '<td class="righter">' + separate(dataJson[i].balance) + '円</td>';
            rowText += '</tr>';
            $("#checked-date").append(rowText);
        }
    })
}

function getSeveralCheckedDate() {
    $.get({
        url: several_checked_date_url,
    }).done((data) => {
        $("#several-checked-date").html(data);
        calculateNowBank(false);
    })
}

function updateCheckedDate(method_id, checkAll) {
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
        getCheckedDate();
        getUncheckedTransaction();
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}

function updateSeveralCheckedDate(id) {
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
        calculateNowBank(true);
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}

function updateLivingCostMark() {
    $.post({
        url: update_living_cost_mark_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "price": Number($("#txt_living_cost").val().replace(",", "")),
        }
    }).done(() => {
        location.reload();
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}
function keyPressLiving(code) {
    // エンターキーなら
    if (code === 13) {
        updateLivingCostMark();
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
        // 確認済み日付も更新
        getCheckedDate()
        // 現在銀行も更新
        getSeveralCheckedDate();
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}

function getUncheckedTransaction() {
    $.get({
        url: unchecked_transaction_url
    }).done((data) => {
        $("#unchecked-transaction").html(data);
    })
}

function calculateNowBank(isAllUpdate) {
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
            getSeveralCheckedDate();
        }
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}

function keyPressNowBank(code) {
    // エンターキーなら
    if (code === 13) {
        calculateNowBank(true);
    }
}
