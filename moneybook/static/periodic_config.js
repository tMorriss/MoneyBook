// 定期取引設定ページのJavaScript

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

$(document).ready(function() {
    const csrftoken = getCookie('csrftoken');
    
    // 行を追加ボタンクリック
    $('#btn_add_row').on('click', function() {
        addNewRow();
    });
    
    // 削除ボタンクリック（動的に追加される要素にも対応）
    $(document).on('click', '.btn-delete', function() {
        if (confirm('この行を削除しますか？')) {
            $(this).closest('tr').remove();
        }
    });
    
    // 更新ボタンクリック
    $('#btn_update').on('click', function() {
        if (!confirm('設定を更新しますか？')) {
            return;
        }
        
        const periodicDataList = [];
        
        // テーブルの各行からデータを取得
        $('#config_tbody tr').each(function() {
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
            }),
            success: function(response) {
                showResultMessage('設定を更新しました', 'success');
                setTimeout(function() {
                    window.location.href = periodic_list_url;
                }, 1000);
            },
            error: function(xhr) {
                const errorMsg = xhr.responseJSON ? JSON.stringify(xhr.responseJSON) : 'エラーが発生しました';
                showResultMessage('更新に失敗しました: ' + errorMsg, 'error');
            }
        });
    });
    
    // 戻るボタンクリック
    $('#btn_back').on('click', function() {
        window.location.href = periodic_list_url;
    });
});

function addNewRow() {
    const newRow = `
        <tr data-id="">
            <td><input type="number" class="input-day" value="1" min="1" max="31"></td>
            <td><input type="text" class="input-item" value="" maxlength="100"></td>
            <td><input type="number" class="input-price" value="0"></td>
            <td>
                <select class="select-direction">
                    ${directions.map(d => `<option value="${d.pk}">${d.name}</option>`).join('')}
                </select>
            </td>
            <td>
                <select class="select-method">
                    ${methods.map(m => `<option value="${m.pk}">${m.name}</option>`).join('')}
                </select>
            </td>
            <td>
                <select class="select-category">
                    ${categories.map(c => `<option value="${c.pk}">${c.name}</option>`).join('')}
                </select>
            </td>
            <td>
                <select class="select-temp">
                    <option value="0" selected>No</option>
                    <option value="1">Yes</option>
                </select>
            </td>
            <td><button class="btn-delete btn-red">削除</button></td>
        </tr>
    `;
    $('#config_tbody').append(newRow);
}
