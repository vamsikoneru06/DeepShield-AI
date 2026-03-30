import numpy as np

def extract_video_features(file_path):
    """
    Dummy deepfake feature simulation
    """
    features = {
        "frame_inconsistency": np.random.uniform(0, 1),
        "color_anomaly": np.random.uniform(0, 1),
        "edge_distortion": np.random.uniform(0, 1),
        "blink_rate": np.random.uniform(0, 1)
    }
    return features


def detect_deepfake(features):
    """
    Simple rule-based detection logic
    """
    score = 0

    if features["frame_inconsistency"] > 0.6:
        score += 30
    if features["color_anomaly"] > 0.6:
        score += 25
    if features["edge_distortion"] > 0.6:
        score += 25
    if features["blink_rate"] < 0.3:
        score += 20

    confidence = min(score, 100)

    if confidence > 60:
        return {
            "result": "DEEPFAKE",
            "confidence": confidence,
            "risk": "HIGH",
            "issues": [
                "Frame inconsistency detected",
                "Color anomaly detected",
                "Facial distortion possible"
            ]
        }
    else:
        return {
            "result": "AUTHENTIC",
            "confidence": confidence,
            "risk": "LOW",
            "issues": []
        }