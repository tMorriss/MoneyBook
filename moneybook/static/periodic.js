// 定期取引一覧ページのJavaScript

// Enterキー押下時の処理
function keyPressAddBulk(keyCode) {
    if (keyCode === 13) { // Enter key
        $('#btn_add_bulk').click();
    }
}

$(document).ready(function() {
    // 追加ボタンクリック
    $('#btn_add_bulk').on('click', function() {
        // 年月を取得（空の場合はplaceholderの値を使用）
        let year = $('#target_year').val();
        let month = $('#target_month').val();

        // 空の場合はplaceholderの値を使用
        if (!year || year.trim() === '') {
            year = $('#target_year').attr('placeholder');
        }
        if (!month || month.trim() === '') {
            month = $('#target_month').attr('placeholder');
        }

        year = parseInt(year);
        month = parseInt(month);

        if (!year || !month || month < 1 || month > 12) {
            showResultMsg('有効な年月を入力してください', empty);
            return;
        }

        // ボタンを無効化
        $('#btn_add_bulk').prop('disabled', true);

        // 登録処理を実行
        const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        $.post({
            url: add_periodic_api_url,
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'year': year,
                'month': month,
            }
        }).done(function() {
            showResultMsg('Success!', empty);
        }).fail(function() {
            showResultMsg('Error...', empty);
        }).always(function() {
            // ボタンを有効化
            $('#btn_add_bulk').prop('disabled', false);
        });
    });
});
