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

$(document).ready(function() {
    const csrftoken = getCookie('csrftoken');
    
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
        $('.tbl-periodic tbody tr').each(function() {
            const id = $(this).data('id');
            if (id) {
                periodicDataList.push({
                    id: id,
                    day: parseInt($(this).find('td:eq(0)').text())
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
    
    // 設定ボタンクリック
    $('#btn_config').on('click', function() {
        window.location.href = periodic_config_url;
    });
});
