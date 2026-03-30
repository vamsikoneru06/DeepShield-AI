from flask import Flask, request, jsonify
from utils.audio_analysis import extract_audio_features, detect_fake_voice
from utils.video_analysis import extract_video_features, detect_deepfake

app = Flask(__name__)

@app.route('/detect-audio', methods=['POST'])
def detect_audio():
    data = request.json
    file_path = data.get("file_path")

    features = extract_audio_features(file_path)
    result = detect_fake_voice(features)

    result["features"] = features
    result["message"] = "⚠️ AI voice detected" if result["result"]=="FAKE" else "✅ Real voice"

    return jsonify(result)


@app.route('/detect-video', methods=['POST'])
def detect_video():
    data = request.json
    file_path = data.get("file_path")

    features = extract_video_features(file_path)
    result = detect_deepfake(features)

    result["features"] = features
    return jsonify(result)


if __name__ == "__main__":
    app.run(port=8000, debug=True)