const express = require('express');
const multer = require('multer');
const cors = require('cors');
const axios = require('axios');
const sqlite3 = require('sqlite3').verbose();

const app = express();
app.use(cors());
app.use(express.json());

const upload = multer({ dest: 'uploads/' });

// DB
const db = new sqlite3.Database('../database/deepshield.db');

// Health
app.get('/api/health', (req, res) => {
    res.json({ status: "Backend running ✅" });
});

// AUDIO
app.post('/api/analyze-audio', upload.single('audio'), async (req, res) => {
    try {
        const response = await axios.post('http://localhost:8000/detect-audio', {
            file_path: req.file.path
        });

        const r = response.data;

        db.run(`INSERT INTO scan_results
        (file_name, file_type, result, confidence_score, risk_level, timestamp)
        VALUES (?, ?, ?, ?, ?, datetime('now'))`,
            [req.file.originalname, 'audio', r.result, r.confidence, r.risk]
        );

        res.json(r);
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

// VIDEO
app.post('/api/analyze-video', upload.single('video'), async (req, res) => {
    try {
        const response = await axios.post('http://localhost:8000/detect-video', {
            file_path: req.file.path
        });

        res.json(response.data);
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

// HISTORY
app.get('/api/history', (req, res) => {
    db.all("SELECT * FROM scan_results ORDER BY timestamp DESC", [], (err, rows) => {
        res.json(rows);
    });
});

app.listen(5000, () => console.log("🚀 Backend running on 5000"));