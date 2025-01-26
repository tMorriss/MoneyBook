function separate(num) {
    return String(num).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
}
function removeComma(num) {
    return num.replace(/,/g, '');
}

function showResultMsg(msg, callback) {
    elm = document.getElementById("result_message");
    elm.innerHTML = msg;
    elm.style.display = "block"; //表示
    fadeInTimer(elm, 0);
    timerId = setTimeout(closeResultMsg, 1000, callback);
}
function closeResultMsg(callback) {
    elm = document.getElementById("result_message");
    fadeOutTimer(elm, 1, callback);
    clearTimeout(timerId);
}

// フェードイン(要素，現在の値)
function fadeInTimer(elm, opaValue) {
    maxMilliSec = 100;
    split = 100;
    if (opaValue < 1) {
        elm.style.opacity = opaValue;
        opaValue = opaValue + (1 / split);
        fadein_timer = setTimeout(function () { fadeInTimer(elm, opaValue); }, (maxMilliSec / split));
    } else {
        clearTimeout(fadein_timer);
        elm.style.opacity = 1;
    }
}
// フェードアウト(要素，現在の値)
function fadeOutTimer(elm, opaValue, callback) {
    maxMilliSec = 100;
    split = 100;
    if (opaValue > 0) {
        elm.style.opacity = opaValue;
        opaValue = opaValue - (1 / split);
        fadeout_timer = setTimeout(function () { fadeOutTimer(elm, opaValue, callback); }, (maxMilliSec / split));
    } else {
        clearTimeout(fadeout_timer);
        elm.style.opacity = 0;
        elm.style.display = "none";
        // リセット処理
        callback();
    }
}

function empty() { }

// テキストの中身を削除
function deleteValue(elm) {
    elm.value = "";
}

function addBlueFocus(id) {
    $(id).addClass('on-fcs-blue');
}
function removeBlueFocus(id) {
    $(id).removeClass('on-fcs-blue');
}

$(() => {
    $('.add_item').autocomplete({
        source: (request, response) => {
            $.get({
                url: suggest_url,
                data: {
                    "item": request.term,
                }
            }).done((data) => {
                const dataJson = JSON.parse(data);
                const items = dataJson.suggests.map(suggest => suggest.item);
                response([...new Set(items)]);
            })
        },
    })
});

$(() => {
    $('.add_price').autocomplete({
        source: (request, response) => {
            $.get({
                url: suggest_url,
                data: {
                    "item": $(".add_item").val(),
                }
            }).done((data) => {
                const dataJson = JSON.parse(data);
                const prices = dataJson.suggests.map(suggest => suggest.price);
                const recentPrice = prices.slice(0, 10);
                response([...new Set(recentPrice)].map(String));
            })
        },
        focus: (event, ui) => {
            $(this).val(ui.item.label);
            return false;
        },
        minLength: 0,
        delay: 0,
    })
});

function zeroPadding(num, length) {
    return ('0'.repeat(length) + num).slice(-length);
}
