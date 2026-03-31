$(document).ready(function() {
    let newRowCounter = 0;

    // 行を追加
    $('#btn_add_row').on('click', function() {
        const template = $('#new_row_template');
        const newRow = template.clone();
        newRow.removeAttr('id');
        newRow.removeAttr('style');

        // name属性にユニークなIDを付与
        newRow.find('input, select').each(function() {
            const name = $(this).attr('name');
            if (name) {
                $(this).attr('name', name.replace('_new', '_new_' + newRowCounter));
            }
        });

        newRow.find('.btn-delete-row').attr('data-new-id', newRowCounter);
        newRowCounter++;

        $('#periodic_table').append(newRow);
    });

    // 削除ボタン
    $(document).on('click', '.btn-delete-row', function() {
        $(this).closest('tr').remove();
    });

    // フォーム送信時に金額を計算
    $('#periodic_edit_form').on('submit', function() {
        $(this).find('input[name^="price_"]').each(function() {
            const evaluated = evaluateFormula($(this).val());
            $(this).val(evaluated);
        });
    });
});
