// Function to update the status of IP addresses dynamically
function updateStatus() {
    for (const ip of ipAddresses) {
        fetch(`/ping?ip=${ip.ip}`)
            .then(response => response.json())
            .then(data => {
                const status = data.status;
                const statusContainer = document.getElementById(`status-${ip.ip}`);

                if (status === "Online") {
                    statusContainer.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="green" class="bi bi-check-circle" viewBox="0 0 16 16"><path d="M8 0a8 8 0 0 1 8 8 8 8 0 0 1-8 8 8 8 0 0 1-8-8 8 8 0 0 1 8-8zM7.293 11.293a.5.5 0 0 0 .708 0L11 7.707l1.293 1.293a.5.5 0 0 0 .708-.708l-2-2a.5.5 0 0 0-.708 0l-2 2a.5.5 0 0 0 0 .708z"/><path d="M7 3a.5.5 0 0 0 .5-.5V1a.5.5 0 0 0-1 0v1.5A.5.5 0 0 0 7 3z"/></svg> Online';
                } else {
                    statusContainer.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="red" class="bi bi-x-circle" viewBox="0 0 16 16"><path d="M8 0a8 8 0 0 1 8 8 8 8 0 0 1-8 8 8 8 0 0 1-8-8 8 8 0 0 1 8-8zM7.354 6.646a.5.5 0 0 0 0 .708L8.707 8l-1.353 1.354a.5.5 0 1 0 .708.708L9 8.707l1.354 1.353a.5.5 0 0 0 .708-.708L9.707 8l1.353-1.354a.5.5 0 0 0-.708-.708L9 7.293 7.646 5.939a.5.5 0 0 0-.292-.093z"/><path d="M8 3.5a.5.5 0 0 0-.5.5V7a.5.5 0 0 0 1 0V4a.5.5 0 0 0-.5-.5z"/></svg> Offline';
                }
            });
    }
}

// Update status every 10 seconds
setInterval(updateStatus, 10000);  // 10 seconds
updateStatus();
