# 🔐 DeepShield AI - Security Hardening Guide

Complete guide for securing DeepShield AI for production use.

---

## 🛡️ Security Layers

```
┌─────────────────────────────────┐
│ 1. Network Security             │ (HTTPS, Firewall, WAF)
├─────────────────────────────────┤
│ 2. Authentication & Authorization│ (JWT, RBAC)
├─────────────────────────────────┤
│ 3. Data Protection              │ (Encryption, Hashing)
├─────────────────────────────────┤
│ 4. Application Security         │ (Input validation, CSRF)
├─────────────────────────────────┤
│ 5. Infrastructure Security      │ (Docker, Secrets)
├─────────────────────────────────┤
│ 6. Monitoring & Logging         │ (Audit trails)
└─────────────────────────────────┘
```

---

## 1️⃣ Network Security

### HTTPS/TLS Configuration

```javascript
// Before: HTTP only
app.listen(5000);

// After: HTTPS
const https = require('https');
const fs = require('fs');

const options = {
  key: fs.readFileSync('./ssl/private.key'),
  cert: fs.readFileSync('./ssl/certificate.crt')
};

https.createServer(options, app).listen(5000);
```

### Nginx Reverse Proxy with SSL

```nginx
upstream backend {
    server localhost:5000;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/ssl/certs/certificate.crt;
    ssl_certificate_key /etc/ssl/private/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    location / {
        proxy_pass https://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Firewall Rules

```bash
# Allow only necessary ports
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Verify rules
sudo ufw status
```

---

## 2️⃣ Authentication & Authorization

### JWT Implementation

```javascript
const jwt = require('jsonwebtoken');

const SECRET_KEY = process.env.JWT_SECRET;

// Generate token
function generateToken(userId) {
  return jwt.sign({ userId }, SECRET_KEY, {
    expiresIn: '24h'
  });
}

// Verify token middleware
function verifyToken(req, res, next) {
  const token = req.headers['authorization']?.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }
  
  try {
    const decoded = jwt.verify(token, SECRET_KEY);
    req.userId = decoded.userId;
    next();
  } catch (err) {
    return res.status(403).json({ error: 'Invalid token' });
  }
}

// Protect routes
app.get('/api/history', verifyToken, (req, res) => {
  // Only authenticated users
  // Use req.userId to identify user
});
```

### Role-Based Access Control (RBAC)

```javascript
// User roles
const ROLES = {
  ADMIN: 'admin',
  USER: 'user',
  VIEWER: 'viewer'
};

// Middleware for role check
function checkRole(allowedRoles) {
  return (req, res, next) => {
    if (!allowedRoles.includes(req.userRole)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}

// Usage
app.delete('/api/history', 
  verifyToken,
  checkRole([ROLES.ADMIN]),
  (req, res) => {
    // Only admins can delete
  }
);
```

---

## 3️⃣ Data Protection

### Password Hashing

```javascript
const bcrypt = require('bcrypt');

// Hash password
async function hashPassword(password) {
  const salt = await bcrypt.genSalt(10);
  return await bcrypt.hash(password, salt);
}

// Verify password
async function verifyPassword(password, hash) {
  return await bcrypt.compare(password, hash);
}
```

### Encryption at Rest

```python
from cryptography.fernet import Fernet

# Generate key
key = Fernet.generate_key()

# Encrypt sensitive data
cipher = Fernet(key)
encrypted_data = cipher.encrypt(b"sensitive data")

# Decrypt
decrypted_data = cipher.decrypt(encrypted_data)
```

### Database Encryption

```sql
-- For PostgreSQL (recommended for production)
-- Enable at database level
CREATE DATABASE deepshield WITH ENCRYPTION = 'on';

-- For SQLite (encrypt with extension)
-- Use sqlcipher extension
sqlite> .open deepshield.db
sqlite> PRAGMA key = 'mypassword';
```

### Environment Variables Security

```bash
# .env file (never commit!)
JWT_SECRET=your-secret-key-here
DB_PASSWORD=secure-password
API_KEY=your-api-key

# Load safely in Node.js
require('dotenv').config();
const secret = process.env.JWT_SECRET;

# In Docker, use secrets
docker secret create jwt_secret ./jwt_secret.txt
```

---

## 4️⃣ Application Security

### Input Validation

```javascript
const { body, validationResult } = require('express-validator');

app.post('/api/analyze-audio', [
  // Validation rules
  body('filename').trim().isLength({ max: 255 }),
  body('filesize').isInt({ min: 1, max: 100000000 }),
  body('filetype').matches(/^audio\/(mpeg|wav|ogg)$/)
], (req, res) => {
  // Check for validation errors
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  
  // Process validated data
});
```

### SQL Injection Prevention (Parameterized Queries)

```javascript
// ❌ VULNERABLE
db.run(`SELECT * FROM users WHERE id = ${userId}`);

// ✅ SAFE
db.run('SELECT * FROM users WHERE id = ?', [userId]);

// ✅ ALSO SAFE (Named parameters)
db.run('SELECT * FROM users WHERE id = :id', { ':id': userId });
```

### Cross-Site Request Forgery (CSRF) Protection

```javascript
const csrf = require('csurf');

// CSRF middleware
const csrfProtection = csrf({ cookie: true });

app.post('/api/analyze-audio', csrfProtection, (req, res) => {
  // Validate CSRF token from request
});
```

### Cross-Site Scripting (XSS) Prevention

```javascript
// ❌ VULNERABLE
res.json({ message: req.query.message });  // User input

// ✅ SAFE - Escape output
const xss = require('xss');
res.json({ message: xss(req.query.message) });

// ✅ SAFE - Content Security Policy
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy', 
    "default-src 'self'; script-src 'self'"
  );
  next();
});
```

### Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per windowMs
  message: 'Too many requests, please try again later'
});

// Apply to all routes
app.use(limiter);

// Or specific routes
app.post('/api/analyze-audio', 
  rateLimit({ max: 5 }), // Max 5 uploads per 15 min
  (req, res) => { /* ... */ }
);
```

### CORS Hardening

```javascript
// ❌ VULNERABLE
app.use(cors());  // Allows all origins

// ✅ SAFE
const cors = require('cors');

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['https://yourdomain.com'],
  methods: ['GET', 'POST', 'DELETE'],
  credentials: true,
  maxAge: 3600
}));
```

---

## 5️⃣ Infrastructure Security

### Docker Security

```dockerfile
# Before: Run as root
FROM node:18
RUN npm install
CMD ["node", "server.js"]

# After: Run as non-root user
FROM node:18-alpine
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

COPY --chown=nodejs:nodejs . .
RUN npm install --production

USER nodejs
EXPOSE 5000
CMD ["node", "server.js"]
```

### Docker Compose Secrets

```yaml
version: '3.8'

services:
  backend:
    image: deepshield-backend
    secrets:
      - jwt_secret
      - db_password
    environment:
      JWT_SECRET_FILE: /run/secrets/jwt_secret
      DB_PASSWORD_FILE: /run/secrets/db_password

secrets:
  jwt_secret:
    external: true
  db_password:
    external: true
```

### Kubernetes Security

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: deepshield-backend
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
  
  containers:
  - name: backend
    image: deepshield-backend:latest
    
    # Security context
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
    
    # Resource limits
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
    
    # Health checks
    livenessProbe:
      httpGet:
        path: /api/health
        port: 5000
      initialDelaySeconds: 30
      periodSeconds: 10
```

---

## 6️⃣ Monitoring & Logging

### Audit Logging

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'audit.log' })
  ]
});

// Log important events
app.post('/api/analyze-audio', (req, res) => {
  logger.info('Audio analysis started', {
    userId: req.userId,
    fileName: req.file.originalname,
    fileSize: req.file.size,
    timestamp: new Date().toISOString()
  });
  
  // ... process ...
  
  logger.info('Audio analysis completed', {
    userId: req.userId,
    result: analysis.result,
    confidence: analysis.confidence_score
  });
});
```

### Error Handling (No Info Leakage)

```javascript
// ❌ VULNERABLE - Exposes internal details
app.get('/api/data', (req, res) => {
  try {
    const data = db.query(...);
  } catch (err) {
    res.status(500).json({ error: err.message }); // ❌ Exposes DB details
  }
});

// ✅ SAFE - Generic error message
app.get('/api/data', (req, res) => {
  try {
    const data = db.query(...);
  } catch (err) {
    logger.error('Database error', { error: err, stack: err.stack });
    res.status(500).json({ error: 'An error occurred' }); // ✅ Generic
  }
});
```

### Security Monitoring

```javascript
// Monitor for suspicious activity
function monitorSecurity() {
  // Track failed attempts
  const failedAttempts = new Map();
  
  app.use((req, res, next) => {
    // Check for SQL injection patterns
    if (/['";]/g.test(req.url + JSON.stringify(req.body))) {
      logger.warn('Potential SQL injection', {
        ip: req.ip,
        url: req.url
      });
    }
    
    // Track repeated failed requests
    const ip = req.ip;
    const key = `${ip}-${req.path}`;
    const count = (failedAttempts.get(key) || 0) + 1;
    
    if (count > 10) {
      logger.error('Suspicious activity detected', {
        ip, count, path: req.path
      });
      // Block IP or challenge with CAPTCHA
    }
    
    failedAttempts.set(key, count);
    next();
  });
}
```

---

## ✅ Security Checklist

### Before Production Deployment

#### Network
- [ ] HTTPS/TLS enabled
- [ ] Strong cipher suites configured
- [ ] Firewall rules in place
- [ ] DDoS protection enabled

#### Authentication & Authorization
- [ ] JWT tokens implemented
- [ ] Token expiration set
- [ ] Role-based access control
- [ ] Multi-factor authentication (future)

#### Data Protection
- [ ] Passwords hashed with bcrypt
- [ ] Sensitive data encrypted
- [ ] Database encryption enabled
- [ ] Secrets management in place

#### Application
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention
- [ ] CSRF protection enabled
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] XSS protection enabled

#### Infrastructure
- [ ] Non-root user in Docker
- [ ] Security context set
- [ ] Resource limits defined
- [ ] Health checks configured
- [ ] Secrets management configured

#### Monitoring
- [ ] Audit logging enabled
- [ ] Error handling secure
- [ ] Intrusion detection active
- [ ] Log aggregation setup
- [ ] Alerting configured

---

## 🔧 Security Configuration Template

```javascript
// config/security.js
module.exports = {
  // CORS
  cors: {
    origin: process.env.ALLOWED_ORIGINS?.split(','),
    credentials: true,
    maxAge: 3600
  },
  
  // JWT
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: '24h',
    refreshExpiresIn: '7d'
  },
  
  // Rate Limiting
  rateLimit: {
    windowMs: 15 * 60 * 1000,
    max: 100,
    message: 'Too many requests'
  },
  
  // HTTPS
  https: {
    certPath: process.env.CERT_PATH,
    keyPath: process.env.KEY_PATH
  },
  
  // Password
  password: {
    minLength: 12,
    requireSpecialChars: true,
    requireNumbers: true
  },
  
  // Database
  database: {
    encrypted: true,
    backupEnabled: true,
    backupInterval: 'daily'
  }
};
```

---

## 📚 Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
- [Express.js Security](https://expressjs.com/en/advanced/best-practice-security.html)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

**Security Hardening Guide Version**: 1.0.0
**Last Updated**: January 2024
**Review Frequency**: Quarterly

---

### Key Principles

1. **Defense in Depth** - Multiple layers of security
2. **Principle of Least Privilege** - Users have minimal permissions
3. **Fail Secure** - Default to deny access
4. **Input Validation** - Never trust user input
5. **Encryption** - Encrypt sensitive data in transit and at rest
6. **Logging & Monitoring** - Track and audit all activities
7. **Regular Updates** - Keep dependencies updated
8. **Incident Response** - Have a plan for security incidents
