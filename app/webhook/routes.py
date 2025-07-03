from flask import Blueprint, request, jsonify
from .extensions import events
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    event_type = request.headers.get('X-GitHub-Event')

   # Shared fields
    author = payload.get("sender", {}).get("login", "Unknown")
    timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")

    data = {
        "author": author,
        "action": event_type,
        "timestamp": timestamp,
        "from_branch": None,
        "to_branch": None,
        "request_id": None,
    }

    if event_type == "PUSH":
        data["to_branch"] = payload.get("ref", "").split("/")[-1]
        data["request_id"] = payload.get("head_commit", {}).get("id", "UNKNOWN")[:7]
    elif event_type == "PULL_REQUEST":
        pr = payload.get("pull_request", {})
        data["from_branch"] = pr.get("head", {}).get("ref")
        data["to_branch"] = pr.get("base", {}).get("ref")
        data["request_id"] = str(pr.get("id", "UNKNOWN"))
    elif event_type == "MERGE":
        # Optional: Add custom logic for merges (GitHub doesn't send "merge" as an event)
        # You'd need to infer from a merged PR or from push to a protected branch
        pass
        
    events.insert_one(data)
    return jsonify({"msg": "Event stored!"}), 200



@routes.route('/logs')
def get_logs():
    return jsonify(list(events.find({}, {"_id": 0})))

