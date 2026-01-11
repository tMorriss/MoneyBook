function separate(num) {
    return String(num).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
}
function removeComma(num) {
    return num.replace(/,/g, '');
}

function evaluateFormula(input) {
    // If input is empty or not a string, return as is
    if (!input || typeof input !== 'string') {
        return input;
    }

    // Trim the input
    input = input.trim();

    // If it doesn't start with '=', just remove commas and return
    if (!input.startsWith('=')) {
        return removeComma(input);
    }

    // Remove the '=' prefix
    let formula = input.substring(1).trim();

    // Remove commas from the formula
    formula = removeComma(formula);

    // Validate that formula only contains allowed characters: digits, operators, parentheses, dots, and whitespace
    // Allowed operators: + - * / ^
    // Hyphen placed at end of character class to match literal minus sign
    if (!/^[\d+*/^().\s-]+$/.test(formula)) {
        // Invalid characters found, return original input without '='
        return removeComma(input.substring(1));
    }

    try {
        // Use a safe math evaluator instead of Function constructor
        const result = evaluateMathExpression(formula);

        // Check if result is a valid number
        if (isNaN(result) || !isFinite(result)) {
            // If result is not a valid number, return original input without '='
            return removeComma(input.substring(1));
        }

        // Return the rounded integer result
        return Math.round(result).toString();
    } catch (e) {
        // If evaluation fails, return original input without '='
        return removeComma(input.substring(1));
    }
}

function evaluateMathExpression(expr) {
    // Replace ^ with ** for power operator
    expr = expr.replace(/\^/g, '**');

    // Tokenize the expression
    const tokens = expr.match(/(\d+\.?\d*|\*\*|[+\-*/()])/g);
    if (!tokens) {
        throw new Error('Invalid expression');
    }

    // Convert to postfix notation (Reverse Polish Notation) using Shunting Yard algorithm
    const output = [];
    const operators = [];
    const precedence = { '+': 1, '-': 1, '*': 2, '/': 2, '**': 3 };
    const rightAssociative = { '**': true };

    for (let i = 0; i < tokens.length; i++) {
        const token = tokens[i];

        if (/^\d+\.?\d*$/.test(token)) {
            // Number
            output.push(parseFloat(token));
        } else if (token in precedence) {
            // Operator
            while (operators.length > 0) {
                const top = operators[operators.length - 1];
                if (top === '(') break;
                if (precedence[top] > precedence[token] ||
                    (precedence[top] === precedence[token] && !rightAssociative[token])) {
                    output.push(operators.pop());
                } else {
                    break;
                }
            }
            operators.push(token);
        } else if (token === '(') {
            operators.push(token);
        } else if (token === ')') {
            while (operators.length > 0 && operators[operators.length - 1] !== '(') {
                output.push(operators.pop());
            }
            operators.pop(); // Remove '('
        }
    }

    while (operators.length > 0) {
        output.push(operators.pop());
    }

    // Evaluate postfix expression
    const stack = [];
    for (let i = 0; i < output.length; i++) {
        const item = output[i];
        if (typeof item === 'number') {
            stack.push(item);
        } else {
            const b = stack.pop();
            const a = stack.pop();
            switch (item) {
                case '+': stack.push(a + b); break;
                case '-': stack.push(a - b); break;
                case '*': stack.push(a * b); break;
                case '/': stack.push(a / b); break;
                case '**': stack.push(Math.pow(a, b)); break;
            }
        }
    }

    return stack[0];
}

// Module-level timer variables
let timerId;
let fadein_timer;
let fadeout_timer;

function showResultMsg(msg, callback) {
    let elm = document.getElementById("result_message");
    elm.innerHTML = msg;
    elm.style.display = "block"; //表示
    fadeInTimer(elm, 0);
    timerId = setTimeout(closeResultMsg, 1000, callback);
}
function closeResultMsg(callback) {
    let elm = document.getElementById("result_message");
    fadeOutTimer(elm, 1, callback);
    clearTimeout(timerId);
}

// フェードイン(要素，現在の値)
function fadeInTimer(elm, opaValue) {
    let maxMilliSec = 100;
    let split = 100;
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
    let maxMilliSec = 100;
    let split = 100;
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
