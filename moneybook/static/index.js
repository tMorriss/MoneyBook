function apply_all(elements, status) {
    for (var i = 0; i < elements.length; i++) {
        elements[i].checked = status;
    }
    apply_filter();
}
function select_all() {
    var elements = document.getElementsByClassName('check_filter');
    apply_all(elements, true);
}
function clear_filter() {
    var elements = document.getElementsByName('filter-class[]');
    apply_all(elements, false);
}
function apply_filter() {
    // 各チェックボックスを取得
    var methodList = document.getElementsByName('filter-method[]');
    var classList = document.getElementsByName('filter-class[]');

    // 履歴表のtr
    var rows = document.getElementsByClassName('data-row');
    for (var i = 0; i < rows.length; i++) {
        methodShowing = false;
        // method
        for (var j = 0; j < methodList.length; j++) {
            if (methodList[j].checked && rows[i].classList.contains(methodList[j].id)) {
                methodShowing = true;
                break;
            }
        }
        classShowing = false;
        // class
        for (var j = 0; j < classList.length; j++) {
            if (classList[j].checked && rows[i].classList.contains(classList[j].id)) {
                classShowing = true;
                break;
            }
        }
        if (methodShowing && classShowing) {
            rows[i].classList.remove("hidden-row");
        }
        else {
            rows[i].classList.add("hidden-row");
        }
    }
}

function update_success() {
    // データ更新
    update_data();
    // メッセージ表示
    show_result_msg("Success!", reset_add_form);
}
