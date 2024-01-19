from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import threading
import time
import random
from datetime import datetime
import socket

app = Flask(__name__)
socketio = SocketIO(app)

ip_addresses = [
    {"name": "Test", "ip": "", "port": ""}
]

announcement_text = "Hope you check all nodes status and uptime here!"

monitoring_interval = 10  # Monitor every 10 seconds
last_ping_statuses = {}
daily_percentages = {}
online_start_times = {}

def is_host_reachable(host, port):
    try:
        with socket.create_connection((host, port), timeout=1) as s:
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def monitor_ips():
    global last_ping_statuses
    global online_start_times
    while True:
        for ip in ip_addresses:
            if is_host_reachable(ip["ip"], ["port"]):  
                last_ping_statuses[ip["ip"]] = "Online"
                if ip["ip"] not in online_start_times:
                    online_start_times[ip["ip"]] = datetime.now()
            else:
                last_ping_statuses[ip["ip"]] = "Offline"
                online_start_times.pop(ip["ip"], None)
            # Simulate daily checks with random percentages (for demonstration purposes)
            daily_percentages[ip["ip"]] = random.randint(80, 100)
            socketio.emit('update_status', {'ip': ip["ip"], 'status': last_ping_statuses[ip["ip"]]}, namespace='/status')
        time.sleep(monitoring_interval)

def calculate_online_days():
    global online_start_times
    while True:
        current_time = datetime.now()
        for ip, start_time in list(online_start_times.items()):
            online_duration = current_time - start_time
            online_days = online_duration.days
            online_start_times[ip] = online_days
        time.sleep(86400)  # Calculate online days once a day

@app.route('/')
def index():
    return render_template('index.html', ip_addresses=ip_addresses, last_ping_statuses=last_ping_statuses, daily_percentages=daily_percentages, online_days=online_start_times, announcement_text=announcement_text)

@socketio.on('connect', namespace='/status')
def handle_connect():
    print('Client connected')

@app.route('/ping', methods=['GET'])
def ping():
    ip = request.args.get('ip')
    status = last_ping_statuses.get(ip, "Unknown")
    return jsonify({'status': status})

if __name__ == '__main__':
    monitor_thread = threading.Thread(target=monitor_ips)
    monitor_thread.daemon = True
    monitor_thread.start()

    online_days_thread = threading.Thread(target=calculate_online_days)
    online_days_thread.daemon = True
    online_days_thread.start()

    socketio.run(app, debug=True, host='0.0.0.0', port=25571, use_reloader=False)
