// Finds all checkboxes in the Photos page to toggle select all button
function photoClickHandler() {
    var selected = document.getElementsByTagName('input');
    for (var i = 0; i < selected.length; ++i) {
        if (selected[i].name.startsWith("selected_photos")) {
            if (selected[i].checked) {
                selected[i].checked = false;
            } else {
                selected[i].checked = true;
            }
            selected[i].onchange();
        }
    }
}

// Finds all checkboxes in the Photos page to enable or disable delete button
function photoButtonChangeHandler(button) {
    if (button.checked) {
        deletebtn.disabled = false;
    } else {
        var selected = document.getElementsByTagName('input');
        var selectedExists = true;
        for (var i = 0; i <= selected.length; ++i) {
            if (selected[i] && selected[i].type != null &&
                selected[i].type == 'checkbox' && selected[i].name.startsWith("selected_photos")) {
                if (selected[i].checked) {
                    selectedExists = false;
                    break;
                }
            }
        }
        if (selectedExists) {
            deletebtn.disabled = true;
        }
    }
}

// Finds all checkboxes in the Events page to toggle select all button
function eventClickHandler() {
    var selected = document.getElementsByTagName('input');
    for (var i = 0; i < selected.length; ++i) {
        if (selected[i].name.startsWith("selected_events")) {
            if (selected[i].checked) {
                selected[i].checked = false;
            } else {
                selected[i].checked = true;
            }
            selected[i].onchange();
        }
    }
}

// Finds all checkboxes in the Events to enable or disable delete button
function eventButtonChangeHandler(button) {
    if (button.checked) {
        deletebtn.disabled = false;
    } else {
        var selected = document.getElementsByTagName('input');
        var selectedExists = true;
        for (var i = 0; i <= selected.length; ++i) {
            if (selected[i] && selected[i].type != null &&
                selected[i].type == 'checkbox' && selected[i].name.startsWith("selected_events")) {
                if (selected[i].checked) {
                    selectedExists = false;
                    break;
                }
            }
        }
        if (selectedExists) {
            deletebtn.disabled = true;
        }
    }
}

// Controls the display of the modal window in user settings page
function userSettingsWindowHandler() {
  var settings = document.getElementById("userSettingsWindow");
  if (settings.style.display === "none") {
    settings.style.display = "block";
  } else {
    settings.style.display = "none";
  }
}

// Closes the modal window when the user clicks the x
function closeModalBox() {
    var settings = document.getElementById("userSettingsWindow");
    settings.style.display = "none";
}

