$newCategory = $('#add_work_new_category');

$(document).ready(function() {
    $('#add_work_category').change(function () {
        if ($(this).val() == 'new') {
            $newCategory.parent().removeClass('hidden');
        }
        else if (!$newCategory.parent().hasClass('hidden')) {
            $newCategory.parent().addClass('hidden');
        }
    });
});