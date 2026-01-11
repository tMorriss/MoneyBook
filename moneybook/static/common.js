function separate(num) {
    return String(num).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
}
function removeComma(num) {
    return num.replace(/,/g, '');
}

function evaluateFormula(input) {
    // 入力が空または文字列でない場合はそのまま返す
    if (!input || typeof input !== 'string') {
        return input;
    }

    // 前後の空白を削除
    input = input.trim();

    // '='で始まらない場合は、カンマを削除して返す
    if (!input.startsWith('=')) {
        return removeComma(input);
    }

    // '='プレフィックスを削除
    let formula = input.substring(1).trim();

    // 数式からカンマを削除
    formula = removeComma(formula);

    // 数式が許可された文字のみを含むか検証: 数字、演算子、括弧、ドット、空白
    // 許可される演算子: + - * /（べき乗は非対応）
    // ハイフンは文字クラスの最後に配置してリテラルのマイナス記号にマッチさせる
    if (!/^[\d+*/().\s-]+$/.test(formula)) {
        // 無効な文字が見つかった場合、'='を除いた元の入力を返す
        return removeComma(input.substring(1));
    }

    try {
        // math.js を使用して数式を安全に評価
        const result = math.evaluate(formula);

        // 結果が有効な数値かチェック
        if (isNaN(result) || !isFinite(result)) {
            // 有効な数値でない場合、'='を除いた元の入力を返す
            return removeComma(input.substring(1));
        }

        // 丸めた整数の結果を返す
        return Math.round(result).toString();
    } catch (e) {
        // 評価が失敗した場合、'='を除いた元の入力を返す
        return removeComma(input.substring(1));
    }
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
