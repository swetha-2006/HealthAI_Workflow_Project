from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# MOCK mode: if OPENAI_API_KEY is not provided, return deterministic output for demos
MOCK_MODE = not bool(os.getenv("OPENAI_API_KEY"))
API_KEY = os.getenv("SECRET_KEY", "demo123")


@app.route("/process", methods=["POST"])
def process():
    # Authorization header
    provided_key = request.headers.get("x-api-key", "")
    if provided_key != API_KEY:
        return jsonify({"status": "error", "message": "Unauthorized - invalid x-api-key header"}), 401

    # Get JSON payload
    data = request.get_json() or {}
    prompt = data.get("prompt", "").strip()
    note_id = data.get("note_id", "")
    timestamp = data.get("timestamp", "")

    if not prompt:
        return jsonify({"status": "error", "message": "Missing prompt in payload"}), 400

    # -------- MOCK MODE RESPONSE (DETERMINISTIC) --------
    if MOCK_MODE:
        article = (
            f"# {prompt}\n\n"
            "## Summary\n"
            f"This is a deterministic demo health note generated in MOCK mode summarizing: \"{prompt}\".\n\n"
            "## Key Points\n"
            "- Point 1: High-level takeaway.\n"
            "- Point 2: Practical advice.\n\n"
            "## Recommendation\n"
            "Follow-up: consult a healthcare professional if symptoms persist.\n\n"
            "*Generated in MOCK mode.*"
        )

        return jsonify({
            "status": "success",
            "message": "Processed in MOCK mode (no OpenAI key required).",
            "note_id": note_id,
            "timestamp": timestamp,
            "article": article
        }), 200

    # -------- REAL MODEL (NOT IMPLEMENTED IN BASIC VERSION) --------
    return jsonify({
        "status": "error",
        "message": "OPENAI_API_KEY detected but live model integration is not included in this basic package."
    }), 501


@app.route("/", methods=["GET"])
def index():
    return "HealthAI Workflow API (mock-enabled) is running."


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)