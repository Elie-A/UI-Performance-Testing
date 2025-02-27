import os
import json
import time
import threading
from flask import Flask, render_template, jsonify
from flask_sock import Sock
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)
sock = Sock(app)

# Configuration
RESULTS_DIR = os.environ.get('RESULTS_DIR', os.path.join(os.getcwd(), 'results'))

# Global state
active_tests = {}
metrics_cache = {}
last_update_time = 0
websockets = []  # Store active WebSocket connections


class MetricsFileHandler(FileSystemEventHandler):
    """Handler for file system events when metrics files are updated."""
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('_metrics.json'):
            load_metrics_file(event.src_path)
            broadcast_metrics()

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('_metrics.json'):
            load_metrics_file(event.src_path)
            broadcast_metrics()


def load_metrics_file(file_path):
    """Load metrics from a file into the cache."""
    global metrics_cache, last_update_time
    
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
            if not content:
                print(f"Warning: Metrics file {file_path} is empty, skipping.")
                return
            test_metrics = json.loads(content)
            test_name = test_metrics.get('test_case_id')
            if test_name:
                metrics_cache[test_name] = test_metrics
                last_update_time = time.time()
                print(f"Loaded metrics for {test_name}")
            else:
                print(f"Warning: No test_case_id found in {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error loading metrics file {file_path}: Invalid JSON - {e}")
    except Exception as e:
        print(f"Error loading metrics file {file_path}: {e}")


def initialize_metrics():
    """Load all existing metrics files from the results directory."""
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR, exist_ok=True)
        return
    
    for filename in os.listdir(RESULTS_DIR):
        if filename.endswith('_metrics.json'):
            file_path = os.path.join(RESULTS_DIR, filename)
            load_metrics_file(file_path)


def start_file_watcher():
    """Start watching the results directory for changes to metrics files."""
    observer = Observer()
    observer.schedule(MetricsFileHandler(), RESULTS_DIR, recursive=False)
    observer.start()
    print(f"Started watching {RESULTS_DIR} for metrics files")
    return observer


def broadcast_metrics():
    """Send updated metrics to all connected WebSocket clients."""
    data = {
        "metrics": metrics_cache,
        "last_update": last_update_time
    }
    for ws in websockets[:]:  # Copy list to avoid modification issues
        try:
            ws.send(json.dumps(data))
        except Exception as e:
            print(f"Error sending to WebSocket: {e}")
            websockets.remove(ws)  # Remove disconnected client


@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('dashboard.html')


@app.route('/api/system_info')
def get_system_info():
    """API endpoint to get the latest system information."""
    system_info = {}
    for test_name, metrics in metrics_cache.items():
        if 'system_info' in metrics:
            system_info = metrics['system_info']
            break
    return jsonify(system_info)


@sock.route('/ws/metrics')
def ws_metrics(ws):
    """WebSocket endpoint to push metrics updates."""
    websockets.append(ws)
    print("WebSocket client connected")
    try:
        # Send initial data
        ws.send(json.dumps({"metrics": metrics_cache, "last_update": last_update_time}))
        while True:
            # Keep connection alive; updates are pushed via broadcast_metrics
            ws.receive()  # Optional: Handle incoming messages if needed
    except Exception as e:
        print(f"WebSocket client disconnected: {e}")
    finally:
        if ws in websockets:
            websockets.remove(ws)


if __name__ == '__main__':
    # Initialize the application
    initialize_metrics()
    observer = start_file_watcher()
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    finally:
        observer.stop()
        observer.join()