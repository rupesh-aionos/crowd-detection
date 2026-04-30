from flask import Flask, request, jsonify
import os
from detector import CrowdDetector
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

PORT = int(os.getenv("PORT", 9009))
MODEL_PATH = os.getenv("MODEL_PATH", "models/yolov8n.pt")
CONF_THRESHOLD = float(os.getenv("CONF_THRESHOLD", 0.3))
CROWD_THRESHOLD = int(os.getenv("CROWD_THRESHOLD", 3))
DISTANCE_THRESHOLD = int(os.getenv("DISTANCE_THRESHOLD", 150))

# Create models directory if it doesn't exist
os.makedirs("models", exist_ok=True)

# Load model once
detector = CrowdDetector(MODEL_PATH, CONF_THRESHOLD, CROWD_THRESHOLD, DISTANCE_THRESHOLD)
model_loaded = True


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "crowd-detection",
        "model_loaded": model_loaded
    })


@app.route("/detect", methods=["POST"])
def detect():
    try:
        if "file" not in request.files:
            return jsonify({"success": False, "error": "file missing"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"success": False, "error": "empty filename"}), 400

        image = Image.open(io.BytesIO(file.read())).convert("RGB")

        result = detector.predict(image)

        return jsonify({
            "success": True,
            "total_people": result["total_people"],
            "crowd_count": result["crowd_count"],
            "crowds": result["crowds"],
            "detections": result["detections"]
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)