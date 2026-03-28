// 定期取引一覧ページのJavaScript

// CSRFトークンを取得する関数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Enterキー押下時の処理
function keyPressAddBulk(keyCode) {
    if (keyCode === 13) { // Enter key
        $('#btn_add_bulk').click();
    }
}

// 編集モードと表示モードを切り替え
function toggleEditMode(isEditMode) {
    if (isEditMode) {
        // 編集モードに切り替え
        $('.view-mode').hide();
        $('.edit-mode').show();
        $('.edit-mode-only').show();
        $('#target_year, #target_month').prop('disabled', true);
    } else {
        // 表示モードに切り替え
        $('.view-mode').show();
        $('.edit-mode').hide();
        $('.edit-mode-only').hide();
        $('#target_year, #target_month').prop('disabled', false);
    }
}

// 新しい行を追加
function addNewRow() {
    // 空の行メッセージを削除
    $('#empty_row').remove();

    const newRow = `
        <tr data-id=""
            data-day="1"
            data-item=""
            data-price="0"
            data-direction="${directions[0].pk}"
            data-method="${methods[0].pk}"
            data-category="${categories[0].pk}"
            data-temp="0">
            <td class="view-mode" style="display:none;">1</td>
            <td class="view-mode" style="display:none;"></td>
            <td class="view-mode righter" style="display:none;">0</td>
            <td class="view-mode" style="display:none;">${directions[0].name}</td>
            <td class="view-mode" style="display:none;">${methods[0].name}</td>
            <td class="view-mode" style="display:none;">${categories[0].name}</td>
            <td class="view-mode" style="display:none;">No</td>
            <td class="edit-mode"><input type="number" class="input-day" value="1" min="1" max="31"></td>
            <td class="edit-mode"><input type="text" class="input-item" value="" maxlength="100"></td>
            <td class="edit-mode"><input type="number" class="input-price" value="0"></td>
            <td class="edit-mode">
                <select class="select-direction">
                    ${directions.map(d => `<option value="${d.pk}">${d.name}</option>`).join('')}
                </select>
            </td>
            <td class="edit-mode">
                <select class="select-method">
                    ${methods.map(m => `<option value="${m.pk}">${m.name}</option>`).join('')}
                </select>
            </td>
            <td class="edit-mode">
                <select class="select-category">
                    ${categories.map(c => `<option value="${c.pk}">${c.name}</option>`).join('')}
                </select>
            </td>
            <td class="edit-mode">
                <select class="select-temp">
                    <option value="0" selected>No</option>
                    <option value="1">Yes</option>
                </select>
            </td>
            <td class="edit-mode-only"><button class="btn-delete btn-red">削除</button></td>
        </tr>
    `;
    $('#periodic_tbody').append(newRow);
}

$(document).ready(function() {
    const csrftoken = getCookie('csrftoken');
    let isEditMode = false;

    // 編集モードボタンクリック
    $('#btn_edit_mode').on('click', function() {
        isEditMode = true;
        toggleEditMode(true);
    });

    // キャンセルボタンクリック
    $('#btn_cancel_edit').on('click', function() {
        if (confirm('編集内容を破棄してよろしいですか？')) {
            location.reload();
        }
    });

    // 行を追加ボタンクリック
    $('#btn_add_row').on('click', function() {
        addNewRow();
    });

    // 削除ボタンクリック（動的に追加される要素にも対応）
    $(document).on('click', '.btn-delete', function() {
        if (confirm('この行を削除しますか？')) {
            $(this).closest('tr').remove();
            // 行がなくなった場合は空メッセージを表示
            if ($('#periodic_tbody tr').length === 0) {
                $('#periodic_tbody').append('<tr id="empty_row"><td colspan="8" class="empty-message">定期取引が設定されていません</td></tr>');
            }
        }
    });

    // 更新ボタンクリック
    $('#btn_update').on('click', function() {
        const periodicDataList = [];

        // テーブルの各行からデータを取得
        $('#periodic_tbody tr').each(function() {
            if ($(this).attr('id') === 'empty_row') {
                return; // 空の行メッセージはスキップ
            }

            const day = parseInt($(this).find('.input-day').val());
            const item = $(this).find('.input-item').val().trim();
            const price = parseInt($(this).find('.input-price').val());
            const direction = parseInt($(this).find('.select-direction').val());
            const method = parseInt($(this).find('.select-method').val());
            const category = parseInt($(this).find('.select-category').val());
            const temp = $(this).find('.select-temp').val() === '1';

            // バリデーション
            if (!day || day < 1 || day > 31) {
                alert('日は1〜31の範囲で入力してください');
                return false;
            }
            if (!item) {
                alert('品目を入力してください');
                return false;
            }
            if (!price || price <= 0) {
                alert('金額は正の数で入力してください');
                return false;
            }

            periodicDataList.push({
                day: day,
                item: item,
                price: price,
                direction: direction,
                method: method,
                category: category,
                temp: temp
            });
        });

        // データ送信
        $.ajax({
            url: periodic_config_url,
            type: 'POST',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: JSON.stringify({
                periodic_data_list: periodicDataList
            })
        }).done(function() {
            showResultMsg('Success!', function() {
                location.reload();
            });
        }).fail(function() {
            showResultMsg('Error...', empty);
        });
    });

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
            alert('有効な年月を入力してください');
            return;
        }

        // 定期取引データを取得
        const periodicDataList = [];
        $('#periodic_tbody tr').each(function() {
            if ($(this).attr('id') === 'empty_row') {
                return; // 空の行メッセージはスキップ
            }
            const id = $(this).data('id');
            if (id) {
                periodicDataList.push({
                    id: id,
                    day: parseInt($(this).data('day'))
                });
            }
        });

        if (periodicDataList.length === 0) {
            alert('定期取引が設定されていません');
            return;
        }

        // 日付順にソート
        periodicDataList.sort((a, b) => a.day - b.day);

        // 進捗エリアを表示
        $('#progress_area').show();
        $('#progress_log').empty();
        $('#btn_add_bulk').prop('disabled', true);

        // 順番に登録処理を実行
        let index = 0;

        function addNext() {
            if (index >= periodicDataList.length) {
                $('#btn_add_bulk').prop('disabled', false);
                showResultMessage('すべての登録が完了しました', 'success');
                return;
            }

            const pd = periodicDataList[index];
            const logMsg = `${pd.day}日のデータを登録中...`;
            $('#progress_log').append(`<p class="progress-item">${logMsg}</p>`);

            $.ajax({
                url: periodic_add_bulk_url,
                type: 'POST',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: JSON.stringify({
                    year: year,
                    month: month,
                    periodic_id: pd.id
                }),
                success: function(response) {
                    $('#progress_log .progress-item:last').append(` ✓ ${response.message}`);

                    index++;
                    setTimeout(addNext, 100); // 少し間隔を空けて次へ
                },
                error: function(xhr) {
                    const errorMsg = xhr.responseJSON ? xhr.responseJSON.error : 'エラーが発生しました';
                    $('#progress_log .progress-item:last').append(` ✗ ${errorMsg}`);
                    $('#btn_add_bulk').prop('disabled', false);
                    showResultMessage('登録中にエラーが発生しました', 'error');
                }
            });
        }

        addNext();
    });
});
