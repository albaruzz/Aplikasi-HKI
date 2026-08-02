import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
from flask import Flask, jsonify, render_template, request
from PIL import Image
from tensorflow.keras.models import load_model
from werkzeug.exceptions import RequestEntityTooLarge

from config import CLASS_0, CLASS_1, IMG_HEIGHT, IMG_WIDTH, MODEL_PATH, RESCALE

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "webp"}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

_model = None


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_model():
    global _model
    if _model is None:
        _model = load_model(MODEL_PATH)
        print(f"Model loaded from {MODEL_PATH}")
    return _model


def preprocess_image(img):
    img = img.convert("RGB")
    img = img.resize((IMG_WIDTH, IMG_HEIGHT), Image.LANCZOS)
    arr = np.asarray(img, dtype=np.float32)
    arr = np.expand_dims(arr, axis=0)
    if RESCALE:
        arr /= 255.0
    return arr


def predict(image_bytes):
    img = Image.open(image_bytes)
    arr = preprocess_image(img)
    prob = float(get_model().predict(arr, verbose=0)[0][0])
    label = CLASS_1 if prob >= 0.5 else CLASS_0
    confidence = prob if label == CLASS_1 else 1.0 - prob
    return {"label": label, "probability": prob, "confidence": confidence}


@app.errorhandler(RequestEntityTooLarge)
def request_entity_too_large(error):
    return jsonify({"error": "Ukuran file melebihi batas maksimal"}), 413


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict_route():
    if "file" not in request.files:
        return jsonify({"error": "Tidak ada bagian file"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Tidak ada file yang dipilih"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Tipe file tidak didukung"}), 400
    try:
        result = predict(file.stream)
    except Exception as exc:
        return jsonify({"error": f"Tidak dapat memproses gambar: {exc}"}), 400
    return jsonify(result)


if __name__ == "__main__":
    get_model()
    app.run(host="127.0.0.1", port=5000, debug=False)
