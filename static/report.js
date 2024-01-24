    var socket = io.connect('http://' + document.domain + ':' + location.port + '/status');

    socket.on('generate_report', function (data) {
        addReport(data.status, data.ip);
    });

    function addReport(status, ip) {
        const reportsContainer = document.getElementById('automaticReports');
        const reportItem = document.createElement('li');
        reportItem.className = 'mb-2 flex items-center';

        const statusIcon = document.createElement('i');
        const statusText = document.createElement('span');
        const timeStamp = document.createElement('span');

        timeStamp.className = 'ml-2 text-gray-500 dark-mode:text-gray-400 text-xs';
        statusIcon.className = 'mr-2 text-lg';

        switch (status) {
            case 'Online':
                statusIcon.className += 'fas fa-check-circle text-green-500';
                reportItem.classList.add('text-green-500');
                break;
            case 'Offline':
                statusIcon.className += 'fas fa-times-circle text-red-500';
                reportItem.classList.add('text-red-500');
                break;
            case 'Maintenance':
                statusIcon.className += 'fas fa-wrench text-yellow-500';
                reportItem.classList.add('text-yellow-500');
                break;
            default:
                break;
        }

        statusText.innerText = `Node ${ip} is ${status}`;
        const date = new Date();
        const formattedDate = `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
        timeStamp.innerText = formattedDate;

        reportItem.appendChild(statusIcon);
        reportItem.appendChild(statusText);
        reportItem.appendChild(timeStamp);

        reportsContainer.appendChild(reportItem);
    }
