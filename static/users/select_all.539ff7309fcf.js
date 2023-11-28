function toggleAllCheckBoxes() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"].others');
    var selectAllCheckBox = document.querySelector('input[type="checkbox"].select-all');

    var allChecked = true;

    if (!selectAllCheckBox.checked) {
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = false;
        }
        allChecked = false;
    } else {
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = true;
        }
        allChecked = true;
    }
}

function toggleCheckboxes() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"].others');
    var selectAllCheckBox = document.querySelector('input[type="checkbox"].select-all');

    var allChecked = true;

    for (var i = 0; i < checkboxes.length; i++) {
        if (!checkboxes[i].checked) {
            allChecked = false;
            break;
        }
    }

    selectAllCheckBox.checked = allChecked;
}