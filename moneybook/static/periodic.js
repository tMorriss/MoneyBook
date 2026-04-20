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

        // 定期取引データを取得
        const periodicDataList = [];
        $('#periodic_table tbody tr').each(function() {
            const day = $(this).data('day');
            const item = $(this).data('item');
            const price = $(this).data('price');
            const direction = $(this).data('direction');
            const method = $(this).data('method');
            const category = $(this).data('category');
            const temp = $(this).data('temp');

            if (day && item && price) {
                periodicDataList.push({
                    day: parseInt(day),
                    item: item,
                    price: parseInt(price),
                    direction: parseInt(direction),
                    method: parseInt(method),
                    category: parseInt(category),
                    temp: temp === 1
                });
            }
        });

        if (periodicDataList.length === 0) {
            showResultMsg('定期取引が設定されていません', empty);
            return;
        }

        // 日付順にソート
        periodicDataList.sort((a, b) => a.day - b.day);

        // ボタンを無効化
        $('#btn_add_bulk').prop('disabled', true);

        // 順番に登録処理を実行
        (async function() {
            let hasError = false;
            const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

            for (let i = 0; i < periodicDataList.length; i++) {
                if (hasError) break;

                const pd = periodicDataList[i];

                // 日付の妥当性チェック
                let day = pd.day;
                const maxDay = new Date(year, month, 0).getDate();
                if (day > maxDay) {
                    day = maxDay;
                }

                try {
                    await $.post({
                        url: add_api_url,
                        data: {
                            'csrfmiddlewaretoken': csrftoken,
                            'date': `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`,
                            'item': pd.item,
                            'price': pd.price,
                            'direction': pd.direction,
                            'method': pd.method,
                            'category': pd.category,
                            'temp': pd.temp ? 'True' : 'False',
                            'checked': 'False',
                        }
                    });
                    // 少し間隔を空けて次へ
                    await new Promise(resolve => setTimeout(resolve, 100));
                } catch (error) {
                    hasError = true;
                    showResultMsg('Error...', empty);
                    break;
                }
            }

            // ボタンを有効化
            $('#btn_add_bulk').prop('disabled', false);

            if (!hasError) {
                showResultMsg('Success!', empty);
            }
        })();
    });
});
