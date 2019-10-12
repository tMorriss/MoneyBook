function show_result_msg(msg, callback) {
    elm = document.getElementById("result_message");
    elm.innerHTML = msg;
    elm.style.display = "block"; //表示
    fadeInTimer(elm, 0);
    timerId = setTimeout(close_result_msg, 1000, callback);
}
function close_result_msg(callback) {
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
        fadein_timer = setTimeout(function(){fadeInTimer(elm, opaValue);}, (maxMilliSec / split));
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
        fadeout_timer = setTimeout(function(){fadeOutTimer(elm, opaValue, callback);}, (maxMilliSec / split));
    } else {
        clearTimeout(fadeout_timer);
        elm.style.opacity = 0;
        //リロード
        callback();
    }
}

function empty() {}