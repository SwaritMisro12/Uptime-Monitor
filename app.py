from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import threading
import time
import random
from datetime import datetime
import socket
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Subject, HtmlContent
import subprocess
import requests

app = Flask(__name__)
socketio = SocketIO(app)

SENDGRID_API_KEY = ""
DISCORD_WEBHOOK_URL = ""


ip_addresses = [
    {"name": "Test", "ip": "0.0.0.0", "port": 22, "category": "test"},
    {"name": "Test1", "ip": "0.0.0.0", "port": 22, "category": "test1"}
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


def send_notification(subject, body):
    svg_style = "width: 50px; height: 50px; margin-right: 10px; vertical-align: middle;"
    sendgrid_logo = '<svg fill="#2E3A59" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 320 110" xml:space="preserve" style="{}"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier">{}</g></svg>'

    message_body = f"""
        <html>
            <body>
                <div style="display: flex; align-items: center;">
                    <div style="{svg_style}">
                        {sendgrid_logo}
                    </div>
                    <div>
                        <h2 style="color: #2E3A59; margin-bottom: 5px;">{subject}</h2>
                        <p style="color: #707070;">{body}</p>
                    </div>
                </div>
            </body>
        </html>
    """

    message = Mail(
        from_email=From("", " Uptime Monitor"),
        to_emails=To("", "Recipient Name"),
        subject=Subject(subject),
        html_content=HtmlContent(message_body)
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print(f"Error sending email: {str(e)}")


def monitor_ips():
    global last_ping_statuses
    global online_start_times

    while True:
        for ip in ip_addresses:
            if is_host_reachable(ip["ip"], ip["port"]):
                if last_ping_statuses.get(ip["ip"], "") != "Online":
                    last_ping_statuses[ip["ip"]] = "Online"
                    online_start_times[ip["ip"]] = datetime.now()
                    send_notification(f"Node {ip['name']} is Online", "Node is now online.")
                    socketio.emit('generate_report', {'ip': ip["ip"], 'status': 'Online'}, namespace='/status')
            else:
                if last_ping_statuses.get(ip["ip"], "") != "Offline":
                    last_ping_statuses[ip["ip"]] = "Offline"
                    online_start_times.pop(ip["ip"], None)
                    send_notification(f"Node {ip['name']} is Offline", "Node is now offline.")
                    socketio.emit('generate_report', {'ip': ip["ip"], 'status': 'Offline'}, namespace='/status')

            daily_percentages[ip["ip"]] = random.randint(10, 100)
            socketio.emit('update_status', {'ip': ip["ip"], 'status': last_ping_statuses[ip["ip"]]}, namespace='/status')

        # Send daily summary every 3 hours
        if datetime.now().hour % 3 == 0 and datetime.now().minute == 0:
            send_notification("Daily Summary", f"Uptime Records: {online_start_times}")
            send_notification("Daily Checks", f"Daily Percentages: {daily_percentages}")

        # Send Discord alert every 5 hours
        if datetime.now().hour % 5 == 0 and datetime.now().minute == 0:
            online_nodes = [f"{name}: {status}" for name, status in last_ping_statuses.items() if status == "Online"]
            offline_nodes = [f"{name}: {status}" for name, status in last_ping_statuses.items() if status == "Offline"]
            content = f"Uptime Monitor Alert\nOnline Nodes: {', '.join(online_nodes)}\nOffline Nodes: {', '.join(offline_nodes)}"
            send_discord_alert(content)

        time.sleep(monitoring_interval)

def get_last_outages(ip):
    global online_start_times
    last_outages = []

    if ip in online_start_times:
        current_time = datetime.now()
        outage_start_time = online_start_times[ip]
        outage_duration = current_time - outage_start_time

        last_outages.append({
            'start_time': outage_start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': current_time.strftime("%Y-%m-%d %H:%M:%S"),
            'duration': str(outage_duration),
        })

    return last_outages


def emit_automatic_report(ip, message):
    # Get the index of the IP in the list for dynamic HTML updates
    index = next((i for i, item in enumerate(ip_addresses) if item["ip"] == ip), None)

    if index is not None:
        socketio.emit('automatic_report', {'index': index, 'message': message}, namespace='/status')


def send_discord_alert(content):
    try:
        payload = {
            'content': content
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending Discord alert: {str(e)}")

def calculate_online_days():
    global online_start_times
    while True:
        current_time = datetime.now()
        for ip, start_time in list(online_start_times.items()):
            online_duration = current_time - start_time
            online_days = online_duration.days
            online_start_times[ip] = online_days
        time.sleep(86400)  # Calculate online days once a day



def handle_generate_report(data):
    ip = data['ip']
    status = data['status']
    last_outages = get_last_outages(ip)

    # Add the 'last_outages' data to your report
    report_data = {
        'ip': ip,
        'status': status,
        'last_outages': last_outages,
    }

    # Broadcast the report data to all connected clients
    socketio.emit('report_generated', report_data, namespace='/status')



@app.route('/')
def index():
    return render_template('index.html', ip_addresses=ip_addresses, last_ping_statuses=last_ping_statuses, daily_percentages=daily_percentages, online_days=online_start_times, announcement_text=announcement_text)

@app.route('/last_outages', methods=['GET'])
def last_outages():
    ip = request.args.get('ip')
    outages = get_last_outages(ip)
    return jsonify({'outages': outages})


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

    socketio.run(app, debug=True, host='0.0.0.0', port=25567, use_reloader=False)
