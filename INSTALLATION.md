# 📦 DeepShield AI - Installation & Deployment Guide

## 🎯 Quick Navigation

- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Docker Deployment](#docker-deployment)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

---

## 📋 Prerequisites

### Minimum System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 500MB
- **Internet**: Required for initial setup

### Required Software

1. **Node.js & npm** (v14+)
   - Download: https://nodejs.org/
   - Verify: `node --version && npm --version`

2. **Python** (3.8+)
   - Download: https://www.python.org/
   - Verify: `python --version`

3. **Git** (optional, for version control)
   - Download: https://git-scm.com/

---

## 🚀 Local Development Setup

### Step 1: Verify Prerequisites

```bash
# Run the verification script
chmod +x verify_setup.sh
./verify_setup.sh

# Or manually check
node --version      # Should be v14+
npm --version       # Should be v6+
python --version    # Should be 3.8+
```

### Step 2: Install Frontend Dependencies

```bash
cd frontend
npm install

# If you encounter issues:
npm install --legacy-peer-deps
npm cache clean --force
```

**Time**: 2-3 minutes
**Expected**: No errors or warnings

### Step 3: Install Backend Dependencies

```bash
cd ../backend
npm install
```

**Time**: 1-2 minutes
**Expected**: Should complete without issues

### Step 4: Setup Python Environment

#### macOS/Linux:
```bash
cd ../ai-service

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Windows:
```cmd
cd ..\ai-service

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Time**: 5-10 minutes (depending on network)
**Note**: Librosa and OpenCV are large packages; be patient

### Step 5: Initialize Database

#### macOS/Linux:
```bash
cd ../database
source ../ai-service/venv/bin/activate
python init_db.py
```

#### Windows:
```cmd
cd ..\database
..\ai-service\venv\Scripts\activate
python init_db.py
```

**Expected Output**:
```
📊 Initializing DeepShield AI Database...
✅ Database initialized successfully at: .../database/deepshield.db
📋 Tables created: scan_results
✅ Added 4 sample records
```

### Step 6: Start Services

Open **3 separate terminal windows** and run:

**Terminal 1 - Backend**:
```bash
cd DeepShield-AI/backend
node server.js

# Expected:
# 🚀 DeepShield AI Backend running on http://localhost:5000
```

**Terminal 2 - AI Service**:
```bash
cd DeepShield-AI/ai-service
source venv/bin/activate    # macOS/Linux
# or
venv\Scripts\activate       # Windows
python app.py

# Expected:
# 🚀 Server starting on http://localhost:8000
```

**Terminal 3 - Frontend**:
```bash
cd DeepShield-AI/frontend
npm start

# Browser should open http://localhost:3000
```

### ✅ Verification

All services should be running at:
- **Frontend**: http://localhost:3000 ✅
- **Backend**: http://localhost:5000 ✅
- **AI Service**: http://localhost:8000 ✅

Test with cURL:
```bash
curl http://localhost:5000/api/health
curl http://localhost:8000/api/health
```

---

## 🐳 Docker Deployment

### Prerequisites
- **Docker**: https://www.docker.com/products/docker-desktop
- **Docker Compose**: Included with Docker Desktop

### Quick Start

```bash
# Build and run all services
docker-compose up --build

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Service Deployment

```bash
# Build individual services
docker build -t deepshield-backend ./backend
docker build -t deepshield-ai ./ai-service
docker build -t deepshield-frontend ./frontend

# Run individual services
docker run -p 5000:5000 deepshield-backend
docker run -p 8000:8000 deepshield-ai
docker run -p 3000:3000 deepshield-frontend
```

### Docker Compose Network

```yaml
# Services communicate via network
deepshield-network:
  - deepshield-frontend (port 3000)
  - deepshield-backend (port 5000)
  - deepshield-ai (port 8000)
  - database (volume)
```

---

## 🌐 Production Deployment

### Cloud Platforms

#### AWS Deployment
```bash
# Using AWS Elastic Container Service (ECS)
1. Create ECR repositories
2. Push Docker images to ECR
3. Create ECS task definitions
4. Deploy using ECS service
5. Setup RDS for PostgreSQL (optional)
6. Configure ALB load balancer
```

#### Google Cloud Deployment
```bash
# Using Google Cloud Run
1. Build Docker image
2. Push to Google Container Registry
3. Deploy using Cloud Run
4. Configure Cloud SQL (optional)
5. Setup Cloud Load Balancing
```

#### Azure Deployment
```bash
# Using Azure Container Instances
1. Build and push to Azure Container Registry
2. Deploy using Container Instances
3. Setup Azure SQL Database (optional)
4. Configure Application Gateway
```

### Environment Variables for Production

#### Backend (.env)
```env
PORT=5000
NODE_ENV=production
AI_SERVICE_URL=http://ai-service:8000
DATABASE_URL=sqlite:///./database/deepshield.db
CORS_ORIGIN=https://yourdomain.com
```

#### AI Service (Dockerfile ENV)
```dockerfile
ENV PORT=8000
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
```

#### Frontend (.env)
```env
REACT_APP_API_URL=https://api.yourdomain.com
NODE_ENV=production
```

### Security Checklist for Production

- [ ] Enable HTTPS/TLS
- [ ] Setup authentication (JWT/OAuth)
- [ ] Configure rate limiting
- [ ] Enable CORS properly
- [ ] Use environment variables for secrets
- [ ] Setup database backups
- [ ] Configure logging & monitoring
- [ ] Setup firewall rules
- [ ] Enable API key management
- [ ] Configure load balancing
- [ ] Setup auto-scaling
- [ ] Enable audit logging

### Nginx Configuration (Reverse Proxy)

```nginx
upstream backend {
    server localhost:5000;
}

upstream ai_service {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # AI Service
    location /ai/ {
        proxy_pass http://ai_service/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🆘 Troubleshooting

### Issue: "Port already in use"

**Solution**:
```bash
# macOS/Linux
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: "Cannot find module"

**Solution**:
```bash
# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install

# Backend
cd backend
rm -rf node_modules package-lock.json
npm install
```

### Issue: "Python virtual environment issues"

**Solution**:
```bash
# Remove and recreate
rm -rf ai-service/venv
cd ai-service
python -m venv venv
source venv/bin/activate      # macOS/Linux
# or
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### Issue: "Database errors"

**Solution**:
```bash
# Reinitialize database
rm database/deepshield.db
python database/init_db.py
```

### Issue: "Backend can't connect to AI service"

**Solution**:
```bash
# Check if AI service is running
curl http://localhost:8000/api/health

# Check backend environment
cat backend/.env

# Verify AI_SERVICE_URL points to correct address
```

### Issue: "Frontend blank page"

**Solution**:
```bash
# Clear browser cache
Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)

# Check frontend logs
npm start

# Check browser console (F12)
```

---

## 📊 Performance Optimization

### Frontend Optimization
```javascript
// Code splitting
React.lazy(() => import('./components/Results'))

// Memoization
React.memo(FileUpload)

// Lazy loading
<img loading="lazy" src={url} />
```

### Backend Optimization
```javascript
// Database indexing (already implemented)
// Connection pooling
// Response compression
app.use(compression());

// Caching
const cache = new Map();
```

### AI Service Optimization
```python
# Model caching
@app.before_first_request
def load_models():
    # Load models once at startup

# Batch processing
# Async processing with Celery
# GPU acceleration (if available)
```

---

## 🔄 Continuous Integration/Deployment

### GitHub Actions Example

```yaml
name: Deploy DeepShield AI

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker images
        run: docker-compose build
      
      - name: Push to registry
        run: |
          docker login -u ${{ secrets.DOCKER_USER }}
          docker-compose push
      
      - name: Deploy to production
        run: docker-compose -H ${{ secrets.DOCKER_HOST }} up -d
```

---

## 📱 Monitoring & Logging

### Application Logs

```bash
# Frontend logs (browser console)
# Backend logs (terminal)
# AI Service logs (terminal)

# Docker logs
docker-compose logs -f
docker logs deepshield-backend
docker logs deepshield-ai
```

### Health Checks

```bash
# Frontend health
curl http://localhost:3000

# Backend health
curl http://localhost:5000/api/health

# AI Service health
curl http://localhost:8000/api/health
```

### Performance Monitoring

```bash
# Check system resources
top
docker stats

# Check network
netstat -an | grep LISTEN
```

---

## 🎯 Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Code review completed
- [ ] Dependencies updated
- [ ] Environment variables configured
- [ ] Database backed up
- [ ] Documentation updated

### Deployment
- [ ] Build Docker images
- [ ] Push to registry
- [ ] Deploy to staging
- [ ] Run smoke tests
- [ ] Deploy to production
- [ ] Monitor for errors

### Post-Deployment
- [ ] Verify all services running
- [ ] Check logs for errors
- [ ] Monitor performance metrics
- [ ] Notify users
- [ ] Document changes

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Express.js Guide](https://expressjs.com/)
- [React Documentation](https://react.dev/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/)

---

## 🎓 Next Steps

1. **Explore the Code**: Review source files in each directory
2. **Test the APIs**: Use cURL or Postman
3. **Customize**: Modify detection algorithms
4. **Integrate**: Add real ML models
5. **Deploy**: Move to production
6. **Monitor**: Setup logging and alerts

---

**Happy Deploying! 🚀**
