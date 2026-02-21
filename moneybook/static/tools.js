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
        url: actual_cash_url,
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
            rowText += '<input type="button" class="btn-green" value="' + dataJson[i].name + '" onclick="updateCheckedDate(' + dataJson[i].pk + ', ' + checkAll + ')">'
            rowText += '</td>';
            rowText += '<td>現在: ' + zeroPadding(dataJson[i].year, 4) + '年' + zeroPadding(dataJson[i].month, 2) + '月' + zeroPadding(dataJson[i].day, 2) + '日</td>';
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
        url: credit_checked_date_url,
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

function keyPressUpdateSeveralCheckedDate(code, id) {
    // エンターキーなら
    if (code === 13) {
        updateSeveralCheckedDate(id);
    }
}

function updateLivingCostMark() {
    $.post({
        url: living_cost_mark_url,
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

function applyCheck() {
    $.post({
        url: edit_apply_check_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
        }
    }).done(() => {
        // 未チェック項目更新
        getUncheckedTransaction();
        // Summaryを更新
        getPreCheckedSummary();
        // 確認済み日付も更新
        getCheckedDate();
        // 現在銀行も更新
        getSeveralCheckedDate();
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}

function preCheck(pk) {
    id = "#a-check-" + pk;
    className = "a-checked";
    nextStatus = 1
    if ($(id).hasClass(className)) {
        nextStatus = 0
    }

    $.post({
        url: edit_pre_check_url,
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "id": pk,
            "status": nextStatus
        }
    }).done(() => {
        // チェックした項目の表示更新
        if ($(id).hasClass(className)) {
            $(id).removeClass(className);
        } else {
            $(id).addClass(className);
        }
        // Summaryを更新
        getPreCheckedSummary();
    }).fail(() => {
        // メッセージ表示
        showResultMsg("Error...", empty);
    });
}

function getUncheckedTransaction() {
    $.get({
        url: unchecked_data_url
    }).done((data) => {
        $("#unchecked-transaction").html(data);
    })
}

function getPreCheckedSummary() {
    $.get({
        url: pre_checked_summary_url
    }).done((data) => {
        $("#pre-checked-summary").html(data);
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
        url: now_bank_url,
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
