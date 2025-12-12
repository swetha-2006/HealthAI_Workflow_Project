# app.py
from flask import Flask, request, jsonify
import os, json
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

MOCK_MODE = not bool(os.getenv("OPENAI_API_KEY"))
API_KEY = os.getenv("SECRET_KEY", "demo123")

SUMMARY_FILE = "summaries.json"


def load_summaries():
    """Load saved summaries from JSON file."""
    if not os.path.exists(SUMMARY_FILE):
        return {}
    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_summaries(data):
    """Save summaries to JSON file."""
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


@app.route("/process", methods=["POST"])
def process():
    provided_key = request.headers.get("x-api-key", "")
    if provided_key != API_KEY:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.get_json() or {}
    prompt = data.get("prompt", "").strip()
    note_id = data.get("note_id", "")
    timestamp = data.get("timestamp", "")

    if not prompt:
        return jsonify({"status": "error", "message": "Missing prompt"}), 400

    # MOCK MODE SUMMARY
    article = (
        f"# {prompt}\n\n"
        "## Summary\n"
        f"This is a deterministic demo summary generated in MOCK mode for: \"{prompt}\".\n\n"
        "## Key Points\n"
        "- Point 1: High-level takeaway.\n"
        "- Point 2: Practical advice.\n\n"
        "## Recommendation\n"
        "Consult a healthcare provider if symptoms persist.\n\n"
        "*Generated in MOCK mode.*"
    )

    # LOAD EXISTING SUMMARIES
    summaries = load_summaries()

    # SAVE NEW ONE
    summaries[note_id] = {
        "note_id": note_id,
        "timestamp": timestamp,
        "prompt": prompt,
        "article": article,
    }

    save_summaries(summaries)

    return jsonify({
        "status": "success",
        "message": "Summary saved",
        "note_id": note_id,
        "article": article
    }), 200


@app.route("/summaries", methods=["GET"])
def summaries_list():
    summaries = load_summaries()
    return jsonify({
        "count": len(summaries),
        "summaries": list(summaries.values())
    })


@app.route("/summaries/<summary_id>", methods=["GET"])
def summaries_get(summary_id):
    summaries = load_summaries()
    if summary_id not in summaries:
        return jsonify({"error": "Not found"}), 404
    return jsonify(summaries[summary_id])


@app.route("/")
def index():
    return "HealthAI Workflow API (mock-enabled) is running."


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
