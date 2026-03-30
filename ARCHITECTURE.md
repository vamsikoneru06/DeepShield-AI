# 🏗️ DeepShield AI - System Architecture & Design Document

## System Overview Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                        CLIENT BROWSER                              │
│                    (User Interface Layer)                          │
│              http://localhost:3000 (React.js)                      │
└────────────────┬─────────────────────────────────────────────────┘
                 │
                 │ HTTP/REST (JSON)
                 │ CORS Enabled
                 │
    ┌────────────▼────────────────────────────────────┐
    │         API GATEWAY / BACKEND SERVER            │
    │         (Node.js + Express - Port 5000)         │
    │                                                 │
    │  ┌─────────────────────────────────────────┐   │
    │  │        Route Handlers                   │   │
    │  ├─────────────────────────────────────────┤   │
    │  │ POST   /api/analyze-audio              │   │
    │  │ POST   /api/analyze-video              │   │
    │  │ GET    /api/history                    │   │
    │  │ GET    /api/stats                      │   │
    │  │ DELETE /api/history                    │   │
    │  │ GET    /api/health                     │   │
    │  └─────────────────────────────────────────┘   │
    │                    │                           │
    │    ┌───────────────┼──────────────┐            │
    │    │               │              │            │
    │    ▼               ▼              ▼            │
    │  ┌──────┐  ┌──────────┐  ┌────────────────┐   │
    │  │Multer│  │  Axios   │  │  sqlite3 Driver│   │
    │  │Upload│  │  Client  │  │  Database ORM  │   │
    │  └──────┘  └──────────┘  └────────────────┘   │
    └────────────┬──────────────┬───────────────────┘
                 │              │
        HTTP POST│              │SQLite Query
                 │              │
    ┌────────────▼──┐  ┌────────▼──────────────────┐
    │   AI SERVICE   │  │    SQLITE DATABASE       │
    │  (Python Flask)│  │  (Port: Filesystem)      │
    │  (Port 8000)   │  │                          │
    │                │  │ ┌─────────────────────┐ │
    │ ┌────────────┐ │  │ │  scan_results Table │ │
    │ │Audio       │ │  │ ├─────────────────────┤ │
    │ │Analyzer    │ │  │ │ id (PRIMARY)        │ │
    │ ├────────────┤ │  │ │ file_name           │ │
    │ │• MFCC      │ │  │ │ file_type           │ │
    │ │• Spectral  │ │  │ │ result              │ │
    │ │• ZCR       │ │  │ │ confidence_score    │ │
    │ │• Features  │ │  │ │ risk_level          │ │
    │ │• Scoring   │ │  │ │ timestamp           │ │
    │ └────────────┘ │  │ │ details (JSON)      │ │
    │                │  │ └─────────────────────┘ │
    │ ┌────────────┐ │  │                         │
    │ │Video       │ │  │ ┌─────────────────────┐ │
    │ │Analyzer    │ │  │ │ Indexes:            │ │
    │ ├────────────┤ │  │ ├─────────────────────┤ │
    │ │• Frames    │ │  │ │ idx_timestamp       │ │
    │ │• Facial    │ │  │ │ idx_result          │ │
    │ │• Color     │ │  │ │ idx_file_type       │ │
    │ │• Edges     │ │  │ │                     │ │
    │ │• Eyes      │ │  │ │ Optimized for speed │ │
    │ │• Scoring   │ │  │ └─────────────────────┘ │
    │ └────────────┘ │  │                         │
    │                │  │                         │
    │ Libraries:     │  │ Path:                   │
    │ • librosa      │  │ ./database/deepshield  │
    │ • OpenCV       │  │ .db                     │
    │ • NumPy        │  └─────────────────────────┘
    │ • SciPy        │
    │ • scikit-learn │
    └────────────────┘
```

---

## 📊 Data Flow Diagram

### Audio File Analysis Flow

```
1. User Upload
   ├─ File: audio.mp3
   ├─ Size: <100MB
   └─ Type: audio/mpeg
        │
        ▼
2. Frontend (React)
   ├─ Validate file
   ├─ Show loading state
   └─ Send to backend
        │
        ▼
3. Backend (Express)
   ├─ Receive multipart form data
   ├─ Validate MIME type
   ├─ Store temporarily
   └─ Forward to AI service
        │
        ▼
4. AI Service (Flask)
   ├─ Load audio file
   ├─ Extract features
   │  ├─ MFCC coefficients (13)
   │  ├─ Spectral centroid
   │  ├─ Spectral rolloff
   │  ├─ Zero crossing rate
   │  └─ Additional features
   ├─ Score confidence (0-100)
   └─ Return is_fake, confidence
        │
        ▼
5. Backend Processing
   ├─ Determine risk_level
   ├─ Store in database
   └─ Return formatted response
        │
        ▼
6. Frontend Display
   ├─ Show FAKE/REAL badge
   ├─ Display confidence meter
   ├─ Show risk level
   ├─ Display alert message
   └─ Switch to results tab
        │
        ▼
7. User Actions
   ├─ Download report
   ├─ View history
   ├─ Check statistics
   └─ Analyze more files
```

### Video File Analysis Flow

```
1. User Upload
   ├─ File: video.mp4
   ├─ Size: <100MB
   └─ Type: video/mp4
        │
        ▼
2. Frontend (React)
   ├─ Validate file
   ├─ Show progress bar
   └─ Send to backend
        │
        ▼
3. Backend (Express)
   ├─ Receive multipart form data
   ├─ Validate MIME type
   ├─ Store temporarily
   └─ Forward to AI service
        │
        ▼
4. AI Service (Flask)
   ├─ Open video with OpenCV
   ├─ Extract frames (every 5th)
   ├─ Limit to 30 frames
   ├─ Analyze each frame
   │  ├─ Color consistency
   │  ├─ Edge distribution
   │  ├─ Eye detection
   │  └─ Facial features
   ├─ Check frame transitions
   ├─ Score confidence (0-100)
   └─ Return is_deepfake, inconsistencies
        │
        ▼
5. Backend Processing
   ├─ Determine risk_level
   ├─ Store in database
   └─ Return formatted response
        │
        ▼
6. Frontend Display
   ├─ Show DEEPFAKE/AUTHENTIC badge
   ├─ Display confidence meter
   ├─ Show risk level
   ├─ List inconsistencies found
   ├─ Display alert message
   └─ Switch to results tab
        │
        ▼
7. User Actions
   ├─ Download report
   ├─ View history
   ├─ Check statistics
   └─ Analyze more files
```

---

## 🔄 Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Dashboard   │  │  FileUpload  │  │   Results    │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                 │              │
│         └──────────┬───────┴─────────┬───────┘              │
│                    │                 │                      │
│              ┌─────▼─────────────────▼──────┐               │
│              │      App.js (Main State)     │               │
│              │  • activeTab                 │               │
│              │  • analysisResult            │               │
│              │  • loading                   │               │
│              │  • error                     │               │
│              │  • historyData               │               │
│              │  • statsData                 │               │
│              └─────┬───────────────┬────────┘               │
│                    │               │                        │
│         ┌──────────▼─┐       ┌─────▼──────────┐            │
│         │  History   │       │  Statistics    │            │
│         │   Component│       │   Component    │            │
│         └──────┬─────┘       └─────┬──────────┘            │
│                │                   │                        │
│                └───────────┬───────┘                        │
└────────────────────────────┼───────────────────────────────┘
                             │
                      HTTP/REST API
                      (Axios Client)
                             │
┌────────────────────────────▼───────────────────────────────┐
│                   BACKEND (Express)                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Routes:  analyze-audio  analyze-video  history  stats    │
│                                                            │
│  Middleware: CORS, Body Parser, Multer                    │
│                                                            │
│  Controllers:                                             │
│  ├─ audioController (500ms-5s)                            │
│  ├─ videoController (1-15s)                               │
│  ├─ historyController (<100ms)                            │
│  └─ statsController (<100ms)                              │
│                                                            │
└────────────────────────────┬──────────────────────────────┘
              ┌──────────────┴──────────────┐
              │                             │
       ┌──────▼──────┐           ┌─────────▼────────┐
       │  AI Service │           │  SQLite Database │
       │  (Axios)    │           │  (sqlite3)       │
       │  Port 8000  │           │  Port: FS        │
       └──────┬──────┘           └─────────┬────────┘
              │                            │
   ┌──────────▼──────────┐        ┌────────▼────────────┐
   │ ML Analysis         │        │ Persistent Storage  │
   ├──────────────────────┤        ├────────────────────┤
   │ • Feature Extract    │        │ • scan_results     │
   │ • Scoring            │        │ • Indexes          │
   │ • Confidence         │        │ • Transactions     │
   │ • Risk Level         │        │ • Backup           │
   └──────────┬──────────┘        └────────┬───────────┘
              │                            │
              └────────────┬───────────────┘
                          │
                    Response (JSON)
                          │
                          ▼
                   Frontend Display
```

---

## 🔌 API Request/Response Flow

### Audio Analysis Request
```
REQUEST (Client → Backend)
─────────────────────────
POST /api/analyze-audio
Content-Type: multipart/form-data

{
  audio: <binary file data>
}

↓ ↓ ↓

PROCESSING (Backend → AI Service)
─────────────────────────────────
POST http://localhost:8000/api/detect-audio
(Forward file to AI service)

↓ ↓ ↓

ML ANALYSIS (AI Service)
────────────────────────
1. Load audio with librosa
2. Extract MFCC features
3. Calculate spectral features
4. Apply scoring algorithm
5. Generate confidence score

↓ ↓ ↓

RESPONSE (AI Service → Backend)
───────────────────────────────
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

↓ ↓ ↓

PROCESSING (Backend)
────────────────────
1. Determine risk_level from confidence
2. Format response
3. Store in database
4. Return to frontend

↓ ↓ ↓

RESPONSE (Backend → Frontend)
─────────────────────────────
HTTP 200 OK
{
  "file_name": "audio.mp3",
  "file_type": "audio",
  "result": "FAKE",
  "confidence_score": 85.3,
  "risk_level": "CRITICAL",
  "message": "⚠️ This content appears to be AI-generated",
  "timestamp": "2024-01-15T10:30:00Z"
}

↓ ↓ ↓

FRONTEND DISPLAY
────────────────
• Switch to Results tab
• Show FAKE badge (red)
• Display confidence meter (85%)
• Show CRITICAL risk level
• Display alert message
• List analysis details
```

---

## 📦 Module Architecture

### Frontend Module Structure
```
src/
├── App.js (Main Component)
│   └── State Management
│       ├── activeTab (upload/results/history/stats)
│       ├── analysisResult
│       ├── loading
│       ├── error
│       ├── historyData
│       └── statsData
│
├── components/
│   ├── Dashboard.js
│   │   ├── Features section
│   │   └── Upload options
│   │
│   ├── FileUpload.js
│   │   ├── Drag-and-drop handler
│   │   ├── File validation
│   │   └── Progress indicator
│   │
│   ├── Results.js
│   │   ├── Result badge
│   │   ├── Confidence meter
│   │   ├── Risk indicator
│   │   ├── Alert message
│   │   ├── Metadata display
│   │   └── Report download
│   │
│   ├── History.js
│   │   ├── Results table
│   │   ├── Filter controls
│   │   ├── Sort options
│   │   ├── Clear history button
│   │   └── Mini confidence bars
│   │
│   └── Statistics.js
│       ├── Stats cards
│       ├── Breakdown cards
│       ├── Distribution charts
│       ├── Confidence meter
│       └── Key insights
│
└── API Integration
    └── axios (HTTP client)
```

### Backend Module Structure
```
server.js
├── Configuration
│   ├── Express setup
│   ├── CORS config
│   ├── Multer config
│   └── Port settings
│
├── Database
│   ├── SQLite connection
│   ├── Table initialization
│   └── Query execution
│
├── Routes
│   ├── POST /api/analyze-audio
│   │   ├── File validation
│   │   ├── Multer processing
│   │   ├── Axios to AI service
│   │   └── Database storage
│   │
│   ├── POST /api/analyze-video
│   │   ├── File validation
│   │   ├── Multer processing
│   │   ├── Axios to AI service
│   │   └── Database storage
│   │
│   ├── GET /api/history
│   │   └── Database query
│   │
│   ├── GET /api/stats
│   │   └── Aggregation query
│   │
│   ├── DELETE /api/history
│   │   └── Delete all records
│   │
│   └── GET /api/health
│       └── Status response
│
└── Error Handling
    └── Try-catch blocks
```

### AI Service Module Structure
```
app.py
├── Configuration
│   ├── Flask setup
│   ├── CORS config
│   └── Upload limits
│
├── AudioAnalyzer Class
│   ├── extract_audio_features()
│   │   ├── Load audio (librosa)
│   │   ├── MFCC extraction
│   │   ├── Spectral features
│   │   ├── ZCR analysis
│   │   ├── Chroma features
│   │   └── Return feature vector
│   │
│   └── detect_fake_voice()
│       ├── Extract features
│       ├── Apply scoring rules
│       ├── Calculate confidence
│       └── Return is_fake, score
│
├── VideoAnalyzer Class
│   ├── extract_frames()
│   │   ├── Open video (OpenCV)
│   │   ├── Sample frames
│   │   ├── Resize frames
│   │   └── Return frame list
│   │
│   └── analyze_facial_features()
│       ├── Frame-to-frame analysis
│       ├── Color consistency check
│       ├── Edge distribution
│       ├── Eye detection
│       ├── Apply scoring
│       └── Return inconsistencies, score
│
└── Routes
    ├── POST /api/detect-audio
    │   └── Call AudioAnalyzer
    │
    ├── POST /api/detect-video
    │   └── Call VideoAnalyzer
    │
    └── GET /api/health
        └── Status response
```

---

## 🗄️ Database Architecture

### Schema Design
```
scan_results
├── id (INTEGER, PRIMARY KEY)
│   └─ Auto-increment, unique identifier
│
├── file_name (TEXT, NOT NULL)
│   └─ Original filename uploaded
│
├── file_type (TEXT, NOT NULL)
│   ├─ 'audio' - Audio file
│   └─ 'video' - Video file
│
├── result (TEXT, NOT NULL)
│   ├─ 'FAKE' - AI-generated voice
│   ├─ 'REAL' - Authentic voice
│   ├─ 'DEEPFAKE' - Manipulated video
│   └─ 'AUTHENTIC' - Genuine video
│
├── confidence_score (REAL, NOT NULL)
│   ├─ Range: 0.0 to 100.0
│   └─ Higher = more likely fake/deepfake
│
├── risk_level (TEXT, NOT NULL)
│   ├─ 'LOW' (≤40%)
│   ├─ 'MEDIUM' (40-60%)
│   ├─ 'HIGH' (60-80%)
│   └─ 'CRITICAL' (>80%)
│
├── timestamp (DATETIME)
│   └─ When scan was performed
│
└── details (TEXT)
    └─ JSON with full analysis data

Indexes:
├── idx_timestamp (timestamp DESC)
│   └─ For fast sorting by date
│
├── idx_result (result)
│   └─ For filtering by result
│
└── idx_file_type (file_type)
    └─ For filtering by type
```

---

## 🔐 Security Architecture

### Input Validation Flow
```
User Input
    │
    ▼
1. File Type Check
   ├─ Audio: mp3, wav, ogg
   ├─ Video: mp4, avi, webm
   └─ Reject others
    │
    ▼
2. File Size Check
   ├─ Maximum: 100MB
   └─ Reject larger
    │
    ▼
3. MIME Type Validation
   ├─ Check Content-Type header
   └─ Verify against whitelist
    │
    ▼
4. Temporary File Handling
   ├─ Store in /tmp
   ├─ Process immediately
   └─ Delete after use
    │
    ▼
5. Database Security
   ├─ Parameterized queries
   ├─ SQL injection prevention
   └─ No direct SQL concatenation
    │
    ▼
Approved Request
```

---

## ⚡ Performance Optimization

### Caching Strategy
```
Frontend Cache:
├─ API responses (memory)
├─ Component state (React)
└─ File preview (temporary)

Backend Cache:
├─ Database query results
├─ File metadata
└─ Connection pooling

AI Service Cache:
├─ Loaded libraries (librosa, OpenCV)
├─ Feature extractors
└─ Model weights (if using real models)
```

### Database Query Optimization
```
Without Indexes:
GET /api/history → Full table scan (slow)

With Indexes:
idx_timestamp → Sort by date (fast)
idx_result → Filter by result (fast)
idx_file_type → Filter by type (fast)

Result: <100ms vs seconds
```

---

## 📈 Scalability Considerations

### Horizontal Scaling
```
Load Balancer
├─ Route requests across multiple backends
├─ Multiple backend instances (5000, 5001, 5002)
└─ Shared database (PostgreSQL)

Multiple AI Services
├─ Parallel processing (8000, 8001, 8002)
└─ Queue system (Redis/RabbitMQ)
```

### Vertical Scaling
```
Optimize Resources:
├─ Increase RAM (larger feature buffers)
├─ CPU cores (parallel processing)
├─ Database tuning (connection pooling)
└─ Network bandwidth (faster file transfers)
```

---

## 🔄 Deployment Architecture

### Local Development
```
Developer Machine
├─ Frontend: npm start (localhost:3000)
├─ Backend: node server.js (localhost:5000)
├─ AI Service: python app.py (localhost:8000)
└─ Database: SQLite file
```

### Docker Deployment
```
Docker Compose
├─ Frontend Container
├─ Backend Container
├─ AI Service Container
└─ Network Bridge (deepshield-network)
```

### Cloud Deployment
```
AWS/GCP/Azure
├─ Container Registry (ECR/GCR/ACR)
├─ Kubernetes Cluster (EKS/GKE/AKS)
├─ Load Balancer (ALB/GLB/LB)
├─ Managed Database (RDS/Cloud SQL/Azure DB)
└─ Cache Layer (ElastiCache/Memorystore)
```

---

## 🎯 Request Latency Breakdown

### Audio Analysis (Typical)
```
Upload:              500ms
Backend Processing:  100ms
Network to AI:       50ms
Audio Analysis:      2-5s
Return to Backend:   50ms
Database Insert:     50ms
Response to Frontend:100ms
─────────────────────────
Total:              ~3-6 seconds
```

### Video Analysis (Typical)
```
Upload:              2-5s
Backend Processing:  100ms
Network to AI:       50ms
Frame Extraction:    2-3s
Feature Analysis:    3-8s
Return to Backend:   50ms
Database Insert:     50ms
Response to Frontend:100ms
─────────────────────────
Total:              ~7-17 seconds
```

---

**Architecture Version**: 1.0.0
**Last Updated**: January 2024
