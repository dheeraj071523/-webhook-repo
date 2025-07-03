from flask import Blueprint, request, jsonify
from .extensions import events
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    event_type = request.headers.get('X-GitHub-Event')

    data = {
        "event_type": event_type,
        "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC"),
        "author": payload.get("sender", {}).get("login", "Unknown")
    }

    if event_type == "push":
        data["to_branch"] = payload.get("ref", "").split("/")[-1]
    elif event_type == "pull_request":
        pr = payload["pull_request"]
        data["from_branch"] = pr["head"]["ref"]
        data["to_branch"] = pr["base"]["ref"]
    elif event_type == "merge":
        # GitHub doesn't send a separate merge event. Bonus if implemented manually
        pass

    events.insert_one(data)
    return jsonify({"msg": "Event stored!"}), 200



@routes.route('/logs')
def get_logs():
    return jsonify(list(events.find({}, {"_id": 0})))

