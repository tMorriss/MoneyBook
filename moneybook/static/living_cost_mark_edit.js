$(function() {
    // 行追加
    $('#btn_add_row').click(function() {
        var newId = new Date().getTime();
        var row = $('#row_template').clone().removeAttr('id').show();
        row.find('input, select').each(function() {
            var name = $(this).attr('name');
            if (name) {
                $(this).attr('name', name.replace('template', newId));
            }
        });
        $('#mark_table_body').append(row);
    });

    // 行削除
    $(document).on('click', '.btn-delete-row', function() {
        $(this).closest('tr').remove();
    });

    // キャンセルボタン
    $('#btn_cancel').click(function() {
        location.href = living_cost_mark_url;
    });
});
