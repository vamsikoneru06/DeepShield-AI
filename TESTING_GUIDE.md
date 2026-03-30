# 🧪 DeepShield AI - Testing Guide

Complete testing procedures for all components of the application.

---

## 📋 Testing Overview

### Test Types
1. **Unit Tests** - Individual function testing
2. **Integration Tests** - Component interaction testing
3. **API Tests** - Endpoint testing
4. **E2E Tests** - Full workflow testing
5. **Load Tests** - Performance testing
6. **Security Tests** - Vulnerability testing

---

## 🔍 Frontend Testing

### Manual UI Testing Checklist

#### Dashboard Component
- [ ] Can see all feature cards
- [ ] Audio upload area visible
- [ ] Video upload area visible
- [ ] Help text displays correctly
- [ ] Responsive on mobile

#### File Upload Component
- [ ] Drag-and-drop accepts files
- [ ] File browser opens on click
- [ ] File size displays
- [ ] File name shows
- [ ] Loading spinner appears during upload
- [ ] Error message on invalid type
- [ ] Error message on oversized file

#### Results Component
- [ ] Alert banner displays
- [ ] Badge shows correct result
- [ ] Confidence score displays
- [ ] Progress bar fills correctly
- [ ] Risk level shows color
- [ ] Message is appropriate
- [ ] Metadata table displays
- [ ] Report download works
- [ ] Back button functional

#### History Component
- [ ] Table shows all records
- [ ] Filter by type works
- [ ] Sort options functional
- [ ] Clear history button works
- [ ] Confirmation dialog appears
- [ ] Risk badges color correctly
- [ ] Timestamps display properly

#### Statistics Component
- [ ] All stat cards visible
- [ ] Numbers calculate correctly
- [ ] Pie chart displays
- [ ] Breakdown cards show
- [ ] Insights text appears
- [ ] Charts are readable

### Automated Frontend Testing

#### Jest Setup
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom jest
```

#### Example Test: Dashboard.test.js
```javascript
import { render, screen } from '@testing-library/react';
import Dashboard from './components/Dashboard';

test('renders feature boxes', () => {
  render(<Dashboard />);
  const boxes = screen.getAllByRole('heading', { level: 3 });
  expect(boxes.length).toBe(4);
});

test('uploads audio file', async () => {
  const mockOnAudio = jest.fn();
  render(<Dashboard onAudioAnalysis={mockOnAudio} />);
  
  const file = new File(['dummy audio'], 'test.mp3', { type: 'audio/mpeg' });
  // Upload file...
  expect(mockOnAudio).toHaveBeenCalledWith(file);
});
```

#### Example Test: FileUpload.test.js
```javascript
test('accepts valid audio file', () => {
  const mockOnSelect = jest.fn();
  render(<FileUpload onFileSelect={mockOnSelect} type="audio" />);
  
  const validFile = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
  // Simulate drag and drop
  expect(mockOnSelect).toHaveBeenCalled();
});

test('rejects invalid file type', () => {
  const mockOnSelect = jest.fn();
  render(<FileUpload onFileSelect={mockOnSelect} type="audio" />);
  
  const invalidFile = new File(['data'], 'test.txt', { type: 'text/plain' });
  // Attempt upload should fail
  expect(mockOnSelect).not.toHaveBeenCalled();
});
```

---

## 🔧 Backend API Testing

### Manual Testing with cURL

#### Test 1: Health Check
```bash
curl -X GET http://localhost:5000/api/health

# Expected Response (200)
{
  "status": "Backend API is running ✅",
  "port": 5000,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Test 2: Invalid Audio Upload
```bash
# Try uploading invalid file type
curl -X POST \
  -F "audio=@test.txt" \
  http://localhost:5000/api/analyze-audio

# Expected Response (400)
{
  "error": "Invalid file type. Only audio and video files allowed."
}
```

#### Test 3: Valid Audio Analysis
```bash
# Create test audio
ffmpeg -f lavfi -i sine=f=1000:d=5 -q:a 9 -acodec libmp3lame test_audio.mp3

# Upload for analysis
curl -X POST \
  -F "audio=@test_audio.mp3" \
  http://localhost:5000/api/analyze-audio

# Expected Response (200)
{
  "file_name": "test_audio.mp3",
  "file_type": "audio",
  "result": "FAKE" or "REAL",
  "confidence_score": 45-95,
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "message": "⚠️ This content...",
  "timestamp": "2024-01-15T10:31:00Z"
}
```

#### Test 4: Valid Video Analysis
```bash
# Create test video
ffmpeg -f lavfi -i color=c=blue:s=320x240:d=5 test_video.mp4

# Upload for analysis
curl -X POST \
  -F "video=@test_video.mp4" \
  http://localhost:5000/api/analyze-video

# Expected Response (200)
{
  "file_name": "test_video.mp4",
  "file_type": "video",
  "result": "DEEPFAKE" or "AUTHENTIC",
  "confidence_score": 20-85,
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "facial_inconsistencies": [...],
  "message": "⚠️ This content...",
  "timestamp": "2024-01-15T10:32:00Z"
}
```

#### Test 5: Get History
```bash
curl http://localhost:5000/api/history

# Expected Response (200)
{
  "total_scans": 5,
  "scans": [
    {
      "id": 1,
      "file_name": "audio1.mp3",
      "result": "FAKE",
      "confidence_score": 85.3,
      ...
    }
  ]
}
```

#### Test 6: Get Statistics
```bash
curl http://localhost:5000/api/stats

# Expected Response (200)
{
  "total_scans": 10,
  "fake_count": 3,
  "deepfake_count": 2,
  "real_count": 3,
  "authentic_count": 2,
  "avg_confidence": 58.5
}
```

### Automated API Testing

#### Supertest Setup
```bash
npm install --save-dev supertest
```

#### Example Test: server.test.js
```javascript
const request = require('supertest');
const app = require('./server');
const fs = require('fs');

describe('API Endpoints', () => {
  
  test('GET /api/health returns 200', async () => {
    const response = await request(app)
      .get('/api/health')
      .expect(200);
    
    expect(response.body.status).toBeDefined();
  });

  test('POST /api/analyze-audio with invalid file returns 400', async () => {
    const response = await request(app)
      .post('/api/analyze-audio')
      .attach('audio', Buffer.from('invalid'), 'test.txt')
      .expect(400);
    
    expect(response.body.error).toBeDefined();
  });

  test('POST /api/analyze-audio with valid file returns 200', async () => {
    const audioPath = './test_audio.mp3';
    
    const response = await request(app)
      .post('/api/analyze-audio')
      .attach('audio', audioPath)
      .expect(200);
    
    expect(response.body.result).toMatch(/FAKE|REAL/);
    expect(response.body.confidence_score).toBeDefined();
  });

  test('GET /api/history returns records', async () => {
    const response = await request(app)
      .get('/api/history')
      .expect(200);
    
    expect(response.body.total_scans).toBeGreaterThanOrEqual(0);
    expect(Array.isArray(response.body.scans)).toBe(true);
  });

  test('GET /api/stats returns statistics', async () => {
    const response = await request(app)
      .get('/api/stats')
      .expect(200);
    
    expect(response.body.total_scans).toBeDefined();
    expect(response.body.avg_confidence).toBeDefined();
  });

  test('DELETE /api/history clears records', async () => {
    const response = await request(app)
      .delete('/api/history')
      .expect(200);
    
    expect(response.body.message).toBeDefined();
  });
});
```

---

## 🤖 AI Service Testing

### Python Unit Tests

#### Setup
```bash
pip install pytest pytest-cov
```

#### Example Test: test_audio_analyzer.py
```python
import pytest
import numpy as np
from ai_service.app import AudioAnalyzer

@pytest.fixture
def analyzer():
    return AudioAnalyzer()

class TestAudioAnalyzer:
    
    def test_extract_features(self, analyzer):
        """Test feature extraction"""
        # Create synthetic audio
        audio_path = 'test_audio.mp3'
        
        features, details = analyzer.extract_audio_features(audio_path)
        
        assert features is not None
        assert len(features) > 0
        assert isinstance(features, np.ndarray)
    
    def test_detect_fake_voice(self, analyzer):
        """Test voice detection"""
        audio_path = 'test_audio.mp3'
        
        result = analyzer.detect_fake_voice(audio_path)
        
        assert 'is_fake' in result
        assert 'confidence_score' in result
        assert 0 <= result['confidence_score'] <= 100
        assert isinstance(result['is_fake'], bool)
```

#### Example Test: test_video_analyzer.py
```python
import pytest
import cv2
from ai_service.app import VideoAnalyzer

@pytest.fixture
def analyzer():
    return VideoAnalyzer()

class TestVideoAnalyzer:
    
    def test_extract_frames(self, analyzer):
        """Test frame extraction"""
        video_path = 'test_video.mp4'
        
        frames = analyzer.extract_frames(video_path)
        
        assert len(frames) > 0
        assert len(frames) <= 30  # Should limit to 30 frames
        assert frames[0].shape[2] == 3  # BGR channels
    
    def test_detect_deepfake(self, analyzer):
        """Test deepfake detection"""
        video_path = 'test_video.mp4'
        
        result = analyzer.detect_deepfake(video_path)
        
        assert 'is_deepfake' in result
        assert 'confidence_score' in result
        assert 'facial_inconsistencies' in result
        assert 0 <= result['confidence_score'] <= 100
```

#### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_service

# Run specific test
pytest test_audio_analyzer.py::TestAudioAnalyzer::test_extract_features
```

---

## 🗄️ Database Testing

### SQL Query Testing

#### Verify Schema
```sql
-- Check table exists
SELECT name FROM sqlite_master WHERE type='table' AND name='scan_results';

-- Check columns
PRAGMA table_info(scan_results);

-- Check indexes
SELECT * FROM sqlite_master WHERE type='index';
```

#### Test Data Operations
```sql
-- Insert test record
INSERT INTO scan_results 
(file_name, file_type, result, confidence_score, risk_level, details)
VALUES ('test.mp3', 'audio', 'FAKE', 85.3, 'CRITICAL', '{}');

-- Verify insert
SELECT * FROM scan_results WHERE file_name='test.mp3';

-- Test filtering
SELECT * FROM scan_results WHERE file_type='audio';

-- Test sorting
SELECT * FROM scan_results ORDER BY timestamp DESC;

-- Test aggregation
SELECT COUNT(*) as total, AVG(confidence_score) as avg_confidence FROM scan_results;

-- Clean up
DELETE FROM scan_results WHERE file_name='test.mp3';
```

---

## ⚡ Performance Testing

### Load Testing with Apache Bench

```bash
# Install Apache Bench
sudo apt-get install apache2-utils  # Linux
brew install httpd  # macOS

# Test health endpoint (100 requests, 10 concurrent)
ab -n 100 -c 10 http://localhost:5000/api/health

# Test with keep-alive
ab -n 100 -c 10 -k http://localhost:5000/api/health

# Output shows:
# - Requests per second
# - Time per request
# - Throughput
# - Transfer rate
```

### Load Testing with Artillery

```bash
npm install -g artillery

# Create load-test.yml
cat > load-test.yml << EOF
config:
  target: 'http://localhost:5000'
  phases:
    - duration: 60
      arrivalRate: 10
scenarios:
  - name: 'API Test'
    flow:
      - get:
          url: '/api/health'
      - get:
          url: '/api/history'
      - get:
          url: '/api/stats'
EOF

# Run test
artillery run load-test.yml
```

---

## 🔐 Security Testing

### OWASP Top 10 Checks

#### 1. Injection (SQL Injection)
```bash
# Try SQL injection
curl -X GET "http://localhost:5000/api/history?id=1'; DROP TABLE scan_results; --"

# Should NOT execute SQL command
# Should return error or empty result
```

#### 2. Broken Authentication
- ✅ No auth required (by design)
- [ ] Should add JWT in production

#### 3. Sensitive Data Exposure
```bash
# Check if sensitive data in logs
curl -X POST \
  -F "audio=@test.mp3" \
  http://localhost:5000/api/analyze-audio 2>&1 | grep -i password

# Should NOT contain sensitive data
```

#### 4. XML External Entities (XXE)
- ✅ Not applicable (no XML parsing)

#### 5. Broken Access Control
- ✅ No authentication (by design)
- [ ] Add in production

#### 6. Security Misconfiguration
```bash
# Check CORS headers
curl -i -X OPTIONS http://localhost:5000/api/health

# Check security headers
curl -i http://localhost:5000/api/health | grep -E 'X-Frame-Options|X-Content-Type-Options'
```

#### 7. Cross-Site Scripting (XSS)
```javascript
// Try XSS in filename
const filename = '<img src=x onerror="alert(1)">';
// Upload file with malicious name

// Frontend should sanitize output
// Backend should escape in responses
```

#### 8. Insecure Deserialization
- ✅ Not vulnerable (JSON only)

#### 9. Using Components with Known Vulnerabilities
```bash
# Check dependencies for vulnerabilities
npm audit

# Update vulnerable packages
npm audit fix
```

#### 10. Insufficient Logging & Monitoring
```bash
# Check if requests are logged
# Monitor backend console for:
# - File uploads
# - API calls
# - Errors
```

---

## 📊 End-to-End Testing

### Complete User Flow Test

#### Step 1: Frontend Upload
1. Navigate to http://localhost:3000
2. See upload interface
3. Drag-drop or click to upload audio

#### Step 2: Backend Processing
1. Check backend logs: "🎙️ Analyzing audio: filename"
2. Request reaches /api/analyze-audio
3. File forwarded to AI service

#### Step 3: AI Service Analysis
1. Check AI service logs: "🎙️ Analyzing audio: filename"
2. Features extracted
3. Confidence calculated

#### Step 4: Backend Response
1. Result received from AI service
2. Stored in database
3. Formatted response sent to frontend

#### Step 5: Frontend Display
1. Results tab activates
2. Badge displays result
3. Confidence meter shows
4. Alert message appears
5. Report can be downloaded

#### Step 6: History Check
1. Navigate to History tab
2. New scan appears in table
3. Can filter and sort
4. Can clear history

#### Step 7: Statistics Check
1. Navigate to Statistics tab
2. Total count increased
3. Detection breakdown updated
4. Charts refreshed

---

## 🔧 Continuous Integration Setup

### GitHub Actions Workflow

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: cd frontend && npm install
      - run: npm test
      - run: npm run build

  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: cd backend && npm install
      - run: npm test

  ai-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r ai-service/requirements.txt
      - run: pytest ai-service/
```

---

## ✅ Testing Checklist

### Before Deployment
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] API tests successful
- [ ] E2E workflow tested
- [ ] Load testing completed
- [ ] Security testing passed
- [ ] No console errors
- [ ] No database errors
- [ ] All features working
- [ ] Documentation updated

---

**Testing Guide Version**: 1.0.0
**Last Updated**: January 2024
