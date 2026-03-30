# 📊 DeepShield AI - API Test Examples & Sample Requests

Complete examples for testing all API endpoints and frontend features.

---

## 🧪 Testing Methods

### 1. Browser (Frontend UI)
### 2. cURL (Command Line)
### 3. Postman (GUI)
### 4. JavaScript (Fetch API)

---

## 📡 BACKEND API TESTS

### Test 1: Health Check

#### cURL
```bash
curl -X GET http://localhost:5000/api/health
```

#### Expected Response
```json
{
  "status": "Backend API is running ✅",
  "port": 5000,
  "timestamp": "2024-01-15T10:30:45.123Z"
}
```

---

### Test 2: Analyze Audio File

#### cURL (macOS/Linux)
```bash
# With an actual audio file
curl -X POST \
  -F "audio=@/path/to/sample.mp3" \
  http://localhost:5000/api/analyze-audio

# With generated test audio
ffmpeg -f lavfi -i sine=f=1000:d=5 -q:a 9 -acodec libmp3lame test.mp3
curl -X POST \
  -F "audio=@test.mp3" \
  http://localhost:5000/api/analyze-audio
```

#### cURL (Windows PowerShell)
```powershell
$file = Get-Item "sample.mp3"
$content = [System.IO.File]::ReadAllBytes($file.FullName)
$boundary = [System.Guid]::NewGuid().ToString()
$body = @"
--$boundary
Content-Disposition: form-data; name="audio"; filename="sample.mp3"
Content-Type: audio/mpeg

$([System.Text.Encoding]::GetEncoding('ISO-8859-1').GetString($content))
--$boundary--
"@

Invoke-WebRequest -Uri "http://localhost:5000/api/analyze-audio" `
  -Method POST `
  -Headers @{"Content-Type" = "multipart/form-data; boundary=$boundary"} `
  -Body $body
```

#### JavaScript (Frontend)
```javascript
const formData = new FormData();
formData.append('audio', audioFile); // audioFile from file input

const response = await fetch('http://localhost:5000/api/analyze-audio', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result);
```

#### Expected Response (Fake Voice Detected)
```json
{
  "file_name": "sample.mp3",
  "file_type": "audio",
  "result": "FAKE",
  "confidence_score": 85.3,
  "risk_level": "CRITICAL",
  "message": "⚠️ This content appears to be AI-generated",
  "timestamp": "2024-01-15T10:30:45.123Z",
  "details": {
    "is_fake": true,
    "confidence_score": 85.3,
    "analysis": {
      "spectral_flatness": 3.2,
      "mfcc_variation": 18.5,
      "zcr_variation": 0.015,
      "spectral_centroid": 3500.0
    }
  }
}
```

#### Expected Response (Real Voice Detected)
```json
{
  "file_name": "real_voice.mp3",
  "file_type": "audio",
  "result": "REAL",
  "confidence_score": 15.2,
  "risk_level": "LOW",
  "message": "✅ Content appears authentic",
  "timestamp": "2024-01-15T10:31:45.123Z",
  "details": {
    "is_fake": false,
    "confidence_score": 15.2,
    "analysis": {
      "spectral_flatness": 15.8,
      "mfcc_variation": 45.2,
      "zcr_variation": 0.045,
      "spectral_centroid": 2800.0
    }
  }
}
```

---

### Test 3: Analyze Video File

#### cURL (macOS/Linux)
```bash
# With an actual video file
curl -X POST \
  -F "video=@/path/to/sample.mp4" \
  http://localhost:5000/api/analyze-video

# With generated test video
ffmpeg -f lavfi -i color=c=blue:s=320x240:d=5 test.mp4
curl -X POST \
  -F "video=@test.mp4" \
  http://localhost:5000/api/analyze-video
```

#### JavaScript (Frontend)
```javascript
const formData = new FormData();
formData.append('video', videoFile); // videoFile from file input

const response = await fetch('http://localhost:5000/api/analyze-video', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result);
```

#### Expected Response (Deepfake Detected)
```json
{
  "file_name": "sample.mp4",
  "file_type": "video",
  "result": "DEEPFAKE",
  "confidence_score": 72.1,
  "risk_level": "HIGH",
  "facial_inconsistencies": [
    "Unnatural frame transitions detected",
    "Color channel anomalies detected",
    "Abnormal edge distribution",
    "Potential eye blinking inconsistencies"
  ],
  "message": "⚠️ This content is likely a DEEPFAKE",
  "timestamp": "2024-01-15T10:32:45.123Z",
  "details": {
    "is_deepfake": true,
    "confidence_score": 72.1,
    "facial_inconsistencies": [
      "Unnatural frame transitions detected",
      "Color channel anomalies detected",
      "Abnormal edge distribution",
      "Potential eye blinking inconsistencies"
    ],
    "frame_analysis": {
      "total_frames_analyzed": 30,
      "frame_transitions": 4.5
    }
  }
}
```

#### Expected Response (Authentic Video)
```json
{
  "file_name": "authentic_video.mp4",
  "file_type": "video",
  "result": "AUTHENTIC",
  "confidence_score": 22.5,
  "risk_level": "LOW",
  "facial_inconsistencies": [],
  "message": "✅ Content appears authentic",
  "timestamp": "2024-01-15T10:33:45.123Z",
  "details": {
    "is_deepfake": false,
    "confidence_score": 22.5,
    "facial_inconsistencies": [],
    "frame_analysis": {
      "total_frames_analyzed": 30,
      "frame_transitions": 2.1
    }
  }
}
```

---

### Test 4: Get Scan History

#### cURL
```bash
curl -X GET http://localhost:5000/api/history
```

#### JavaScript
```javascript
const response = await fetch('http://localhost:5000/api/history', {
  method: 'GET'
});

const data = await response.json();
console.log(data);
```

#### Expected Response
```json
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
      "timestamp": "2024-01-15T10:30:45.123Z",
      "details": "{\"is_fake\": true, ...}"
    },
    {
      "id": 2,
      "file_name": "sample.mp4",
      "file_type": "video",
      "result": "DEEPFAKE",
      "confidence_score": 72.1,
      "risk_level": "HIGH",
      "timestamp": "2024-01-15T10:32:45.123Z",
      "details": "{\"is_deepfake\": true, ...}"
    }
  ]
}
```

---

### Test 5: Get Statistics

#### cURL
```bash
curl -X GET http://localhost:5000/api/stats
```

#### JavaScript
```javascript
const response = await fetch('http://localhost:5000/api/stats', {
  method: 'GET'
});

const stats = await response.json();
console.log(stats);
```

#### Expected Response
```json
{
  "total_scans": 10,
  "fake_count": 3,
  "deepfake_count": 2,
  "real_count": 3,
  "authentic_count": 2,
  "avg_confidence": 58.5
}
```

---

### Test 6: Clear History

#### cURL
```bash
curl -X DELETE http://localhost:5000/api/history
```

#### JavaScript
```javascript
const response = await fetch('http://localhost:5000/api/history', {
  method: 'DELETE'
});

const result = await response.json();
console.log(result);
```

#### Expected Response
```json
{
  "message": "History cleared successfully"
}
```

---

## 🤖 AI SERVICE API TESTS

### Test 1: Audio Detection (Direct)

#### cURL
```bash
curl -X POST \
  -F "audio_file=@sample.mp3" \
  http://localhost:8000/api/detect-audio
```

#### Expected Response
```json
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

---

### Test 2: Video Detection (Direct)

#### cURL
```bash
curl -X POST \
  -F "video_file=@sample.mp4" \
  http://localhost:8000/api/detect-video
```

#### Expected Response
```json
{
  "is_deepfake": true,
  "confidence_score": 72.1,
  "facial_inconsistencies": [
    "Unnatural frame transitions detected",
    "Color channel anomalies detected",
    "Abnormal edge distribution",
    "Potential eye blinking inconsistencies"
  ],
  "frame_analysis": {
    "total_frames_analyzed": 30,
    "frame_transitions": 4.5
  }
}
```

---

## 🎨 FRONTEND TESTING

### Test 1: Upload Audio via UI

**Steps:**
1. Open http://localhost:3000
2. Click on "🎙️ Voice Analysis" section
3. Drag & drop an audio file (or click Browse Files)
4. Wait for analysis
5. View results with confidence score

**Expected UI:**
- File appears in upload area
- Loading spinner shows
- Results tab activates automatically
- Displays: FAKE/REAL, confidence %, risk level
- Shows alert message

---

### Test 2: Upload Video via UI

**Steps:**
1. Open http://localhost:3000
2. Click on "🎥 Video Deepfake Detection" section
3. Drag & drop a video file (or click Browse Files)
4. Wait for analysis
5. View results with facial inconsistencies

**Expected UI:**
- File appears in upload area
- Loading spinner shows
- Results tab activates automatically
- Displays: DEEPFAKE/AUTHENTIC, confidence %, risk level
- Shows list of detected inconsistencies

---

### Test 3: View History

**Steps:**
1. Open http://localhost:3000
2. Click "📜 History" tab
3. See all past scans in table

**Features to test:**
- Filter by file type (Audio/Video)
- Sort by date/confidence/result
- Clear history button
- Risk level color coding

---

### Test 4: View Statistics

**Steps:**
1. Open http://localhost:3000
2. Click "📈 Statistics" tab
3. See dashboard with metrics

**Elements to verify:**
- Total scans count
- Average confidence
- Fake/Deepfake count
- Real/Authentic count
- Pie chart visualization
- Confidence meter
- Key insights

---

## 📝 Sample Test Data

### Audio File Descriptions

| Filename | Type | Expected Result | Confidence |
|----------|------|-----------------|-----------|
| voice_fake_1.mp3 | Synthetic speech | FAKE | 85-95% |
| voice_fake_2.mp3 | TTS generated | FAKE | 75-85% |
| voice_real_1.mp3 | Human voice | REAL | 5-25% |
| voice_real_2.mp3 | Recorded speech | REAL | 10-30% |

### Video File Descriptions

| Filename | Type | Expected Result | Confidence |
|----------|------|-----------------|-----------|
| deepfake_1.mp4 | Face-swapped | DEEPFAKE | 80-95% |
| deepfake_2.mp4 | Synthetic face | DEEPFAKE | 70-85% |
| authentic_1.mp4 | Real video | AUTHENTIC | 5-25% |
| authentic_2.mp4 | Genuine recording | AUTHENTIC | 10-30% |

---

## 🔍 Debugging & Monitoring

### Check Backend Logs
```bash
# Terminal running backend
# Look for:
# - 🎙️ Analyzing audio: filename
# - 🎥 Analyzing video: filename
# - ✅ Analysis complete
# - ❌ Error messages
```

### Check AI Service Logs
```bash
# Terminal running AI service
# Look for:
# - 🎙️ Analyzing audio: filename
# - 🎥 Analyzing video: filename
# - Analysis metrics
# - ❌ Error messages
```

### Check Frontend Console
```javascript
// Press F12 in browser, go to Console tab
// Look for:
// - Network requests to /api/analyze-*
// - Response data logged
// - Any JavaScript errors
```

---

## 📊 Example Test Sequence

### Full Test Flow

1. **Backend Health Check**
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **AI Service Health Check**
   ```bash
   curl http://localhost:8000/api/health
   ```

3. **Test Audio Analysis**
   ```bash
   ffmpeg -f lavfi -i sine=f=1000:d=5 -q:a 9 -acodec libmp3lame test.mp3
   curl -X POST -F "audio=@test.mp3" http://localhost:5000/api/analyze-audio
   ```

4. **Test Video Analysis**
   ```bash
   ffmpeg -f lavfi -i color=c=blue:s=320x240:d=5 test.mp4
   curl -X POST -F "video=@test.mp4" http://localhost:5000/api/analyze-video
   ```

5. **Get History**
   ```bash
   curl http://localhost:5000/api/history
   ```

6. **Get Statistics**
   ```bash
   curl http://localhost:5000/api/stats
   ```

7. **Test Frontend UI**
   - Open http://localhost:3000
   - Upload files
   - Verify results match API responses

---

## ✅ Success Criteria

Your setup is working correctly if:

| Test | ✅ Pass Criteria |
|------|---|
| Backend Health | Returns 200 with status message |
| AI Service Health | Returns 200 with status message |
| Audio Upload | Returns confidence score |
| Video Upload | Returns confidence score |
| History | Shows all past scans |
| Statistics | Shows accurate counts |
| Frontend UI | Displays results correctly |
| File Filtering | Can filter by type |
| Data Export | Can download JSON report |

---

## 🐛 Common Test Issues & Solutions

### Issue: File upload returns 400
**Solution:** Check file format, size < 100MB, and MIME type

### Issue: Analysis takes too long
**Solution:** This is normal for first run (libraries loading). Subsequent analyses are faster

### Issue: Results show different confidence values
**Solution:** Expected - demo uses randomization. In production, use trained models

### Issue: Error connecting to AI service
**Solution:** Make sure AI service is running on port 8000

---

## 📚 Additional Resources

- [API Documentation](./README.md#-api-documentation)
- [Troubleshooting Guide](./README.md#-troubleshooting)
- [Quick Start Guide](./QUICKSTART.md)

---

**Happy Testing! 🧪**
