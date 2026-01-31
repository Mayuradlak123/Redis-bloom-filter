import time
import json
import random
from flask import Blueprint, Response, render_template

events_bp = Blueprint('events', __name__)

@events_bp.route('/sse')
def sse_page():
    """Render the SSE demo page."""
    return render_template('sse.html')

def event_stream():
    """Generator for server-sent events."""
    topics = ["Global Metrics", "User Activity", "Security Audit", "System Health"]
    while True:
        # Simulate some data
        data = {
            "time": time.strftime('%H:%M:%S'),
            "topic": random.choice(topics),
            "message": f"New update received from {random.choice(['Node-A', 'Node-B', 'Edge-1'])}",
            "value": random.randint(10, 100)
        }
        # SSE format: "data: <content>\n\n"
        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(2)  # Send every 2 seconds

@events_bp.route('/stream')
def stream():
    """SSE endpoint that returns a stream of events."""
    return Response(event_stream(), mimetype='text/event-stream')
