var socket = io.connect('http://' + document.domain + ':' + location.port + '/status');

socket.on('update_status', function (data) {
    // Update status text
    var statusText = document.getElementById('status-' + data.ip);
    if (statusText) {
        statusText.innerText = data.status;
    }

    // Display alert for both online and offline hosts
    var alertText = document.getElementById('alert-text');
    if (data.status === 'Offline') {
        alertText.innerText = 'Host ' + data.ip + ' is offline!';
        document.getElementById('alert-container').style.display = 'block';
    } else if (data.status === 'Online') {
        alertText.innerText = 'Host ' + data.ip + ' is back online!';
        document.getElementById('alert-container').style.display = 'block';
    } else {
        document.getElementById('alert-container').style.display = 'none';
    }
});

function dismissAlert() {
    document.getElementById('alert-container').style.display = 'none';
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}

function hideAnnouncement() {
    var announcementContainer = document.getElementById('announcement-container');
    if (announcementContainer) {
        announcementContainer.style.display = 'none';
    }
}

// After the announcement is displayed, set a timeout to hide it after 30 seconds
setTimeout(hideAnnouncement, 30000);