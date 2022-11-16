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


// Modal window to ask the user to confirm delete on events list & photo list pages
function confirmDelete(btn) {
    if (confirm('Are you sure you want to delete this?')){
        btn.href = btn.getAttribute('zref')
    }
}

// Modal window to ask the user to confirm delete on event & photo details pages
// Source: https://stackoverflow.com/questions/37398416/django-delete-confirmation
$(document).on('click', '.item-detail-confirm-delete', function(){
    return confirm('Are you sure you want to delete this?');
})


// Get the session cookie for creating the page components
// Source: https://www.advantch.com/blog/how-to-set-up-user-notifications-for-your-django-app-part-2/
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

// Calculates & Formats timesince event in user notifications drop down
function prettyDate(dateMs)
{
    var msPerSec = 1000;
    var msPerMin = msPerSec*60;
    var msPerHr = msPerMin*60;
    var msPerDay = msPerHr*24;

    var remainder = dateMs;
    var numDays = Math.floor(remainder/msPerDay);
    remainder %= msPerDay;
    var numHours = Math.floor(remainder/msPerHr);
    remainder %= msPerHr;
    var numMin = Math.floor(remainder/msPerMin);
    remainder %= msPerMin;
    var numSec = Math.floor(remainder/msPerSec);
    remainder %= msPerSec;

    // Formats output of timesince
    var prefix = '';
    if (numDays > 0) {
        prefix = ' day'
        if (numDays > 1) {
            prefix = prefix + 's'
        }
        return numDays + prefix + ' ago';
    } else if (numHours > 0) {
        prefix = ' hour'
        if (numHours > 1) {
            prefix = prefix + 's'
        }
        return numHours + prefix + ' ago';
    } else if (numMin > 0) {
        prefix = ' minute'
        if (numMin > 1) {
            prefix = prefix + 's'
        }
        return numMin + prefix + ' ago';
    } else if (numSec > 0) {
        prefix = ' second'
        if (numSec > 1) {
            prefix = prefix + 's'
        }
        return numSec + prefix + ' ago';
    } else {
        return remainder + ' milliseconds ago';
    }
}

// Connect the session component to fetch user notifications from the database
// Source: Modified from: https://www.advantch.com/blog/how-to-set-up-user-notifications-for-your-django-app-part-2/
const csrf_token = getCookie('csrftoken');
function fetchLatest(alpine_bell) {
    fetch(location.origin + '/inbox/notifications/api/all_list/', {
            method: 'GET',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrf_token,
            },
        }).then(response => response.json())
        .then(data => {

            // Open the notifications dropdown and fetch all notifications
            var notifications = data['all_list'];
            console.log(notifications)

            if (!alpine_bell.isOpen) {
                alpine_bell.notifications = notifications;
            } else {
                alpine_bell.pendingNotifications = notifications;
            }

            // Check if any notifications are unread
            var hasUnread = false;
            for (var x = 0; x < notifications.length; ++x) {
                if (notifications[x].unread)
                    hasUnread = true;
            }
            // Add the red dot for new notifications
            alpine_bell.hasUnreadNotifications = hasUnread;
            if (hasUnread) {
                    $('#unread_dot').addClass('animate-pulse expanding red-filter')

            }
            return data
        }).catch(err => {
            console.log(err);
        })
}

// Mark notifications as read
// Source: Modified from: https://www.advantch.com/blog/how-to-set-up-user-notifications-for-your-django-app-part-2/
function markAsRead() {
    fetch(location.origin + '/inbox/notifications/mark-all-as-read/', {
            method: 'GET',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrf_token,
            },
        }).then(response => response)
        .then(data => {
            return data
        }).catch(err => {
            console.log(err);
        })
}

// Timer to search for new notifications
var notifications_dropdown = null;
setInterval(fetchLatestNotificationsTimer, 5000);
function fetchLatestNotificationsTimer() {
    fetchLatest(notifications_dropdown);
}


setInterval(updateNotificationTimeSince, 500);
function updateNotificationTimeSince() {
    if (notifications_dropdown != null) {
        var notifications = notifications_dropdown.notifications;
        for (var x=0; x<notifications.length; ++x) {
            var HLA = $('#how-long-ago' + x);
            HLA.text(function(){ var current=new Date(); var ts=new Date(notifications[x].timestamp); return prettyDate(current-ts); });
        }
    }
}

// Connect the notification icon with the notifications dropdown
// Source: Modified from: https://www.advantch.com/blog/how-to-set-up-user-notifications-for-your-django-app-part-2/
document.addEventListener('alpine:initializing', () => {
    Alpine.data('user_notifications_dropdown', () => ({

        isOpen: false, //drop down state
        hasUnreadNotifications: false, // red dot will show if this is true
        notifications: [], // list of notifications
        pendingNotifications: null,

        init() {
            notifications_dropdown = this;
            fetchLatest(this);
        },
        // Toggles the notifications drop down
        toggle() {
            this.isOpen = !this.isOpen
            // If the user has notifications, show the red dot on the bell
            // If the user toggles the drop down, mark notifications as read
            if (this.isOpen) {
                if (this.pendingNotifications!=null){
                    this.notifications = this.pendingNotifications;
                    this.pendingNotifications = null;
                }
                var dot = $('#unread_dot');
                if (dot.hasClass('red-filter')){
                    markAsRead();
                    dot.removeClass('animate-pulse expanding red-filter')
                }
            }
        }
    }))
})
