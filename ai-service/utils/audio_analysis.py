import numpy as np

def extract_audio_features(file_path):
    """
    Dummy feature extraction (simulate MFCC, spectral features)
    """
    features = {
        "mfcc_mean": np.random.uniform(10, 50),
        "spectral_centroid": np.random.uniform(2000, 5000),
        "zero_crossing_rate": np.random.uniform(0.01, 0.1),
        "spectral_flatness": np.random.uniform(0, 10)
    }
    return features


def detect_fake_voice(features):
    """
    Simple rule-based detection (easy for viva explanation)
    """
    score = 0

    if features["mfcc_mean"] < 25:
        score += 30
    if features["spectral_centroid"] > 3500:
        score += 30
    if features["zero_crossing_rate"] < 0.03:
        score += 20
    if features["spectral_flatness"] < 3:
        score += 20

    confidence = min(score, 100)

    if confidence > 60:
        return {
            "result": "FAKE",
            "confidence": confidence,
            "risk": "HIGH"
        }
    else:
        return {
            "result": "REAL",
            "confidence": confidence,
            "risk": "LOW"
        }