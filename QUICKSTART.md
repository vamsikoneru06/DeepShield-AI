# 🚀 DeepShield AI - Quick Start Guide

A beginner-friendly step-by-step setup guide to get the project running in minutes.

## ⏱️ Estimated Setup Time: 15-20 minutes

---

## Step 1: Prerequisites Check (2 min)

### Windows Users
```cmd
# Check Node.js
node --version
npm --version

# Check Python
python --version
```

### macOS/Linux Users
```bash
# Check Node.js
node --version
npm --version

# Check Python
python3 --version
```

---

## Step 2: Navigate to Project (1 min)

```bash
cd DeepShield-AI
```

---

## Step 3: Install Frontend Dependencies (3-4 min)

```bash
cd frontend
npm install
```

**Expected Output:**
```
added XXX packages, and audited XXX packages in XXs
found 0 vulnerabilities
```

---

## Step 4: Install Backend Dependencies (2-3 min)

```bash
cd ../backend
npm install
```

---

## Step 5: Install Python Dependencies (4-5 min)

### For macOS/Linux:

```bash
cd ../ai-service

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### For Windows:

```cmd
cd ..\ai-service

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Note:** Installation may take a few minutes (librosa, opencv, scikit-learn are large packages)

---

## Step 6: Initialize Database (1 min)

### macOS/Linux:
```bash
cd ../database
source ../ai-service/venv/bin/activate
python init_db.py
```

### Windows:
```cmd
cd ..\database
..\ai-service\venv\Scripts\activate
python init_db.py
```

**Expected Output:**
```
📊 Initializing DeepShield AI Database...
✅ Database initialized successfully at: .../database/deepshield.db
📋 Tables created: scan_results
✅ Added 4 sample records
```

---

## Step 7: Start Backend (Terminal 1)

### macOS/Linux:
```bash
cd DeepShield-AI/backend
node server.js
```

### Windows:
```cmd
cd DeepShield-AI\backend
node server.js
```

**Expected Output:**
```
🚀 DeepShield AI Backend running on http://localhost:5000
📊 Database: .../database/deepshield.db

📚 Available Endpoints:
   POST   /api/analyze-audio
   POST   /api/analyze-video
   GET    /api/history
   GET    /api/stats
   DELETE /api/history
```

✅ **Backend is ready!**

---

## Step 8: Start AI Service (Terminal 2)

### macOS/Linux:
```bash
cd DeepShield-AI/ai-service
source venv/bin/activate
python app.py
```

### Windows:
```cmd
cd DeepShield-AI\ai-service
venv\Scripts\activate
python app.py
```

**Expected Output:**
```
╔════════════════════════════════════════════════════════════╗
║          🤖 DeepShield AI - Python AI Service              ║
║  🚀 Server starting on http://localhost:8000               ║
║  📊 ML Models: Audio & Video Analysis                      ║
║  🔬 Features: MFCC, Spectral, Facial Consistency Analysis  ║
╚════════════════════════════════════════════════════════════╝
```

✅ **AI Service is ready!**

---

## Step 9: Start Frontend (Terminal 3)

### macOS/Linux:
```bash
cd DeepShield-AI/frontend
npm start
```

### Windows:
```cmd
cd DeepShield-AI\frontend
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view deepshield-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

✅ **Frontend is ready!**

---

## 🎯 All Services Running!

You should now have all three services running:

| Service | URL | Status |
|---------|-----|--------|
| 🎨 Frontend (React) | http://localhost:3000 | ✅ Running |
| 🔧 Backend (Node.js) | http://localhost:5000 | ✅ Running |
| 🤖 AI Service (Python) | http://localhost:8000 | ✅ Running |

---

## 📱 Using the Application

### 1. Open Frontend
Open your browser and navigate to **http://localhost:3000**

You should see the DeepShield AI dashboard with:
- 🎙️ Voice Analysis section
- 🎥 Video Deepfake Detection section
- 📊 Drag-and-drop upload areas

### 2. Upload a File

**Audio:**
- Click on "🎙️ Voice Analysis" section
- Drag and drop an audio file (.mp3, .wav, .ogg)
- Or click "Browse Files" to select from disk

**Video:**
- Click on "🎥 Video Deepfake Detection" section
- Drag and drop a video file (.mp4, .avi, .webm)
- Or click "Browse Files" to select from disk

### 3. View Results

After upload:
1. Backend receives the file
2. AI Service analyzes it
3. Results display with:
   - Detection result (FAKE/REAL or DEEPFAKE/AUTHENTIC)
   - Confidence score (%)
   - Risk level (LOW/MEDIUM/HIGH/CRITICAL)
   - ⚠️ Alert message if malicious

### 4. View History

Click "📜 History" tab to see:
- All past scans
- Filter by audio/video
- Sort by date, confidence, or result

### 5. View Statistics

Click "📈 Statistics" tab to see:
- Total scans
- Detection breakdown
- Average confidence
- Visual charts

---

## 🧪 Testing Without Real Files

### Option 1: Create Simple Test Files

#### Generate Test Audio (requires ffmpeg)
```bash
# macOS/Linux
ffmpeg -f lavfi -i sine=frequency=1000:duration=5 -q:a 9 -acodec libmp3lame test_audio.mp3

# Windows (in Command Prompt)
ffmpeg -f lavfi -i sine=frequency=1000:duration=5 -q:a 9 -acodec libmp3lame test_audio.mp3
```

#### Generate Test Video (requires ffmpeg)
```bash
# macOS/Linux
ffmpeg -f lavfi -i color=c=blue:s=320x240:d=5 test_video.mp4

# Windows (in Command Prompt)
ffmpeg -f lavfi -i color=c=blue:s=320x240:d=5 test_video.mp4
```

### Option 2: Use Sample Files

The database comes with 4 sample records. Check the History tab to see them!

### Option 3: Test via cURL

```bash
# Test health
curl http://localhost:5000/api/health
curl http://localhost:8000/api/health

# Test with a file (macOS/Linux)
curl -X POST -F "audio=@test_audio.mp3" http://localhost:5000/api/analyze-audio

# Windows PowerShell
$file = Get-Item "test_audio.mp3"
$content = [System.IO.File]::ReadAllBytes($file.FullName)
Invoke-WebRequest -Uri "http://localhost:5000/api/analyze-audio" -Method POST -Form @{"audio"=$content}
```

---

## ⚙️ Environment Variables

### Backend (.env file already created)
```
PORT=5000
AI_SERVICE_URL=http://localhost:8000
NODE_ENV=development
```

### Frontend (uses default values)
```
REACT_APP_API_URL=http://localhost:5000/api
```

### Python Service (uses default values)
```
PORT=8000
FLASK_ENV=development
```

---

## 🆘 Quick Troubleshooting

### Problem: "Port 5000 already in use"

**macOS/Linux:**
```bash
# Find process
lsof -i :5000

# Kill it
kill -9 <PID>
```

**Windows:**
```cmd
# Find process
netstat -ano | findstr :5000

# Kill it
taskkill /PID <PID> /F
```

### Problem: Python virtual environment not activating

```bash
# Make sure you're in ai-service directory
cd ai-service

# Try activation again (macOS/Linux)
source venv/bin/activate

# Try activation again (Windows)
venv\Scripts\activate
```

### Problem: npm dependencies fail

```bash
# Clear cache and reinstall
npm cache clean --force
rm -rf node_modules
npm install
```

### Problem: Frontend won't connect to backend

1. **Check backend is running** on http://localhost:5000
2. **Check AI service is running** on http://localhost:8000
3. **Check firewall** is allowing local connections
4. **Hard refresh browser** (Ctrl+Shift+R or Cmd+Shift+R)

---

## 📚 What's Next?

After getting familiar with the basic setup:

### Explore the Code
- **Frontend**: Check `/frontend/src/components/` for React components
- **Backend**: Check `/backend/server.js` for API endpoints
- **AI Service**: Check `/ai-service/app.py` for ML logic

### Try Advanced Features
- Filter scan history
- Download analysis reports
- View detailed statistics
- Analyze multiple files

### Customize
- Change detection thresholds in `ai-service/app.py`
- Modify UI styling in CSS files
- Add new API endpoints
- Integrate real ML models

---

## 🎓 Learning Resources

### Frontend (React)
- React Hooks: useState, useEffect
- Axios for API calls
- Component composition

### Backend (Node.js/Express)
- Express middleware
- File upload handling (multer)
- Database integration (SQLite)
- CORS configuration

### AI Service (Python)
- Librosa for audio processing
- OpenCV for video processing
- scikit-learn for ML utilities
- Feature extraction techniques

---

## 💡 Tips for Success

1. **Keep terminals organized**: Use separate terminal windows for each service
2. **Monitor logs**: Check console output for errors
3. **Test incrementally**: Test one feature at a time
4. **Clear browser cache**: If UI doesn't update properly
5. **Check all 3 services**: Make sure all are running before testing

---

## 🎉 You're All Set!

Congratulations! You have successfully set up DeepShield AI!

### Next Steps:
1. ✅ Open http://localhost:3000
2. ✅ Upload sample audio/video
3. ✅ View results
4. ✅ Check history and stats
5. ✅ Explore the code

**Happy Detecting! 🛡️**

---

## 📞 Need Help?

Check the main [README.md](./README.md) for:
- Detailed API documentation
- Advanced features
- Production deployment
- Troubleshooting guide
