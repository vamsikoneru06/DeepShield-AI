# 🛡️ DeepShield AI - Real-Time Deepfake & Voice Scam Detection System

A full-stack cybersecurity application for detecting AI-generated voice scams and deepfake videos in real-time with risk assessment and detailed analytics.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Features Overview](#features-overview)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### 🎙️ **Voice Analysis Module**
- Detect AI-generated or deepfake voice scams
- Spectral and temporal feature extraction
- MFCC analysis, Zero-crossing rate detection
- Confidence scoring (0-100%)
- Real-time processing

### 🎥 **Video Deepfake Detection Module**
- Identify manipulated video content
- Analyze facial inconsistencies
- Frame-to-frame consistency checking
- Eye blinking and lip-sync anomaly detection
- Confidence scoring with detailed breakdown

### 📊 **Interactive Dashboard**
- Drag-and-drop file upload (Audio & Video)
- Real-time analysis results
- Risk level indicators (Low/Medium/High/Critical)
- Confidence meters with visual feedback
- ⚠️ AI-generated content alerts

### 📜 **Scan History & Analytics**
- Complete scan history with filtering
- Statistics dashboard with trends
- Risk distribution charts
- Detection metrics and insights
- Export reports as JSON

### 🔐 **Backend API (Node.js + Express)**
- RESTful API endpoints
- File handling with multer
- Cross-origin request support (CORS)
- SQLite database integration
- Error handling and validation

### 🤖 **AI Microservice (Python Flask)**
- Dedicated ML processing service
- Audio feature extraction (librosa)
- Video frame analysis (OpenCV)
- Scalable architecture
- Easy to integrate with ML models

### 💾 **Database (SQLite)**
- Persistent scan results storage
- Indexed queries for performance
- Metadata preservation
- Analysis details in JSON format

---

## 🛠 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | React 18 | Interactive UI Dashboard |
| **Backend** | Node.js + Express | REST API Server |
| **Database** | SQLite | Local Data Storage |
| **AI Service** | Python + Flask | ML Detection Engine |
| **Libraries** | Librosa, OpenCV, scikit-learn | Audio/Video Processing |

---

## 📁 Project Structure

```
DeepShield-AI/
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── index.css
│   │   └── components/
│   │       ├── Dashboard.js
│   │       ├── Dashboard.css
│   │       ├── FileUpload.js
│   │       ├── FileUpload.css
│   │       ├── Results.js
│   │       ├── Results.css
│   │       ├── History.js
│   │       ├── History.css
│   │       ├── Statistics.js
│   │       └── Statistics.css
│   ├── public/
│   │   └── index.html
│   └── package.json
│
├── backend/
│   ├── server.js
│   ├── package.json
│   └── .env
│
├── ai-service/
│   ├── app.py
│   └── requirements.txt
│
├── database/
│   ├── deepshield.db (created after init)
│   └── init_db.py
│
└── README.md
```

---

## 📦 Prerequisites

Make sure you have the following installed:

### System Requirements
- **Node.js** v14+ and **npm** v6+
- **Python** 3.8+
- **Git** (optional)

### Check Installation
```bash
# Check Node.js
node --version
npm --version

# Check Python
python --version
```

---

## 🚀 Installation & Setup

### Step 1: Clone or Download Project
```bash
cd DeepShield-AI
```

### Step 2: Setup Frontend (React)

```bash
cd frontend
npm install

# Optional: If you face issues with dependencies
npm install --legacy-peer-deps
```

### Step 3: Setup Backend (Node.js)

```bash
cd ../backend
npm install
```

### Step 4: Setup AI Service (Python)

```bash
cd ../ai-service

# Create Python virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 5: Initialize Database

```bash
cd ../database

# Activate Python environment from ai-service
# On macOS/Linux:
source ../ai-service/venv/bin/activate

# On Windows:
..\ai-service\venv\Scripts\activate

# Run initialization script
python init_db.py
```

---

## ▶️ Running the Application

### Terminal 1: Start Backend (Node.js + Express)

```bash
cd DeepShield-AI/backend
node server.js

# Expected Output:
# 🚀 DeepShield AI Backend running on http://localhost:5000
# ✅ Connected to SQLite Database
```

### Terminal 2: Start AI Service (Python Flask)

```bash
cd DeepShield-AI/ai-service

# Activate virtual environment first
# macOS/Linux: source venv/bin/activate
# Windows: venv\Scripts\activate

python app.py

# Expected Output:
# ╔════════════════════════════════════════════════════════════╗
# ║          🤖 DeepShield AI - Python AI Service              ║
# ║  🚀 Server starting on http://localhost:8000               ║
```

### Terminal 3: Start Frontend (React)

```bash
cd DeepShield-AI/frontend
npm start

# This will automatically open http://localhost:3000 in your browser
# Expected: React app loads with DeepShield AI interface
```

### ✅ All Services Running

You should now have:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **AI Service**: http://localhost:8000

---

## 📡 API Documentation

### Backend API (Node.js) - `localhost:5000`

#### 1. Health Check
```
GET /api/health
Response: { status: "Backend API is running ✅" }
```

#### 2. Analyze Audio
```
POST /api/analyze-audio
Content-Type: multipart/form-data

Parameters:
- audio (file): Audio file (.mp3, .wav, .ogg)

Response:
{
  "file_name": "sample.mp3",
  "file_type": "audio",
  "result": "FAKE",
  "confidence_score": 85.3,
  "risk_level": "CRITICAL",
  "message": "⚠️ This content appears to be AI-generated",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 3. Analyze Video
```
POST /api/analyze-video
Content-Type: multipart/form-data

Parameters:
- video (file): Video file (.mp4, .avi, .webm)

Response:
{
  "file_name": "sample.mp4",
  "file_type": "video",
  "result": "DEEPFAKE",
  "confidence_score": 72.1,
  "risk_level": "HIGH",
  "facial_inconsistencies": [
    "Unnatural frame transitions detected",
    "Eye blinking inconsistencies"
  ],
  "message": "⚠️ This content is likely a DEEPFAKE",
  "timestamp": "2024-01-15T10:31:00Z"
}
```

#### 4. Get History
```
GET /api/history
Response:
{
  "total_scans": 5,
  "scans": [
    {
      "id": 1,
      "file_name": "sample.mp3",
      "file_type": "audio",
      "result": "FAKE",
      "confidence_score": 85.3,
      "risk_level": "CRITICAL",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### 5. Get Statistics
```
GET /api/stats
Response:
{
  "total_scans": 10,
  "fake_count": 3,
  "deepfake_count": 2,
  "real_count": 3,
  "authentic_count": 2,
  "avg_confidence": 58.5
}
```

#### 6. Clear History
```
DELETE /api/history
Response: { message: "History cleared successfully" }
```

---

### AI Service API (Python Flask) - `localhost:8000`

#### 1. Detect Audio Deepfake
```
POST /api/detect-audio
Content-Type: multipart/form-data

Parameters:
- audio_file (file): Audio file

Response:
{
  "is_fake": true,
  "confidence_score": 85.3,
  "analysis": {
    "spectral_flatness": 3.2,
    "mfcc_variation": 18.5,
    "zcr_variation": 0.015,
    "spectral_centroid": 3500.0
  }
}
```

#### 2. Detect Video Deepfake
```
POST /api/detect-video
Content-Type: multipart/form-data

Parameters:
- video_file (file): Video file

Response:
{
  "is_deepfake": true,
  "confidence_score": 72.1,
  "facial_inconsistencies": [
    "Unnatural frame transitions detected",
    "Color channel anomalies detected",
    "Potential eye blinking inconsistencies"
  ],
  "frame_analysis": {
    "total_frames_analyzed": 30,
    "frame_transitions": 4.5
  }
}
```

---

## 💡 Usage Examples

### Example 1: Analyzing an Audio File via cURL

```bash
curl -X POST \
  -F "audio=@sample_voice.mp3" \
  http://localhost:5000/api/analyze-audio
```

### Example 2: Analyzing a Video File via cURL

```bash
curl -X POST \
  -F "video=@sample_video.mp4" \
  http://localhost:5000/api/analyze-video
```

### Example 3: Getting Scan History

```bash
curl http://localhost:5000/api/history
```

### Example 4: Getting Statistics

```bash
curl http://localhost:5000/api/stats
```

---

## 🧪 Testing

### Test Files (Create Sample Files)

#### Create Test Audio File
```bash
# Using ffmpeg (if installed)
ffmpeg -f lavfi -i sine=frequency=1000:duration=5 -q:a 9 -acodec libmp3lame test_audio.mp3

# Or download sample audio from online sources
```

#### Create Test Video File
```bash
# Using ffmpeg
ffmpeg -f lavfi -i color=c=blue:s=320x240:d=5 test_video.mp4
```

### Testing via Frontend

1. **Open http://localhost:3000** in your browser
2. **Upload audio/video files** using drag-and-drop or file browser
3. **View results** with confidence scores and risk levels
4. **Check history** tab for all past scans
5. **View statistics** for analytics dashboard

### Testing via Backend API (Postman/cURL)

```bash
# Test health endpoints
curl http://localhost:5000/api/health
curl http://localhost:8000/api/health

# Test audio analysis
curl -X POST -F "audio=@test_audio.mp3" http://localhost:5000/api/analyze-audio

# Test video analysis
curl -X POST -F "video=@test_video.mp4" http://localhost:5000/api/analyze-video
```

---

## 📊 Features Overview

### Dashboard Features

| Feature | Description |
|---------|-------------|
| **Drag-and-Drop Upload** | Upload audio/video files easily |
| **Real-Time Analysis** | Instant deepfake detection |
| **Confidence Meter** | Visual progress bar showing confidence |
| **Risk Indicators** | Color-coded risk levels |
| **Detailed Results** | Comprehensive analysis breakdown |
| **Download Reports** | Export results as JSON |

### History Features

| Feature | Description |
|---------|-------------|
| **Scan History Table** | View all past scans |
| **Filtering** | Filter by file type (audio/video) |
| **Sorting** | Sort by date, confidence, or result |
| **Quick Stats** | Showing count of detected issues |
| **Clear History** | Delete all records with confirmation |

### Statistics Features

| Feature | Description |
|---------|-------------|
| **Total Scans** | Count of all analyzed files |
| **Avg Confidence** | Average detection confidence |
| **Fake/Deepfake Count** | Malicious content statistics |
| **Real/Authentic Count** | Legitimate content statistics |
| **Distribution Chart** | Pie chart visualization |
| **Key Insights** | AI-generated summary of findings |

---

## 🔍 ML Models & Detection Logic

### Audio Analysis
- **MFCC (Mel-Frequency Cepstral Coefficients)**: Voice characteristic analysis
- **Spectral Centroid**: Frequency distribution analysis
- **Zero Crossing Rate**: Voice stability analysis
- **Chroma Features**: Pitch consistency analysis

### Video Analysis
- **Frame Consistency**: Analyzing transitions between frames
- **Color Channel Analysis**: Detecting compression artifacts
- **Edge Distribution**: Identifying unnatural patterns
- **Facial Features**: Detecting anomalies in eyes and expressions

---

## 🐛 Troubleshooting

### Issue: Backend fails to start

**Solution:**
```bash
# Check if port 5000 is in use
# macOS/Linux:
lsof -i :5000

# Kill process on port 5000:
kill -9 <PID>

# Try starting again:
node server.js
```

### Issue: Python service fails to start

**Solution:**
```bash
# Ensure virtual environment is activated
source ai-service/venv/bin/activate  # macOS/Linux
# or
ai-service\venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r ai-service/requirements.txt

# Try starting again
python ai-service/app.py
```

### Issue: Frontend won't connect to backend

**Solution:**
```bash
# Check if backend is running on port 5000
curl http://localhost:5000/api/health

# Clear browser cache and hard refresh (Ctrl+Shift+R)

# Check CORS settings in backend/server.js (should be enabled)

# Try restarting frontend:
npm start
```

### Issue: Database errors

**Solution:**
```bash
# Delete old database and reinitialize
rm database/deepshield.db

# Reinitialize database
python database/init_db.py

# Restart backend
node backend/server.js
```

### Issue: File upload fails

**Solution:**
```bash
# Check file size (max 100MB)
# Check file format (mp3, wav, ogg, mp4, avi, webm)
# Check if backend is receiving the request (check console logs)
```

---

## 🚀 Performance Tips

1. **Reduce Video Duration**: Shorter videos analyze faster
2. **Use Compressed Audio**: Reduces processing time
3. **Limit History**: Clear old scans periodically
4. **Database Indexing**: Already optimized in schema
5. **ML Model Caching**: Pre-load models in production

---

## 📝 Next Steps & Enhancements

### Phase 2 (Advanced)
- [ ] Integrate trained ML models (TensorFlow, PyTorch)
- [ ] Add real-time webcam detection
- [ ] Implement WebSocket for live updates
- [ ] Add user authentication
- [ ] Database replication & backup

### Phase 3 (Production)
- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] Redis caching layer
- [ ] PostgreSQL migration
- [ ] Advanced monitoring & logging

---

## 📄 License

This project is open-source and available for educational purposes.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## 📧 Support

For issues or questions, please refer to the troubleshooting section or create an issue in the repository.

---

## 🎓 Educational Note

This is a **demonstration/educational project** designed for college-level cybersecurity courses. The ML models use heuristic-based detection for demo purposes. For production use, integrate professional ML models trained on real datasets.

---

**Made with 🛡️ for Cybersecurity Education**
