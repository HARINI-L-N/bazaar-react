# 🚀 START HERE - Quick Setup Guide

## ⚡ Fastest Way to Get Running

### Option 1: Automated Script (Recommended)

**Windows:**
```powershell
# Just double-click this file:
backend\setup-and-run.bat
```

This will:
1. ✅ Activate virtual environment
2. ✅ Install all dependencies
3. ✅ Set up .env file
4. ✅ Populate database
5. ✅ Start backend server

### Option 2: Manual Setup

**Step 1: Install MongoDB**
- Download: https://www.mongodb.com/try/download/community
- OR use cloud version: https://www.mongodb.com/atlas

**Step 2: Setup Backend**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install Flask Flask-MongoEngine Flask-JWT-Extended Flask-CORS python-dotenv Werkzeug
copy env.example .env
# Edit .env with MongoDB connection
python populate_db.py
python app.py
```

**Step 3: Setup Frontend** (in new terminal)
```powershell
npm install
npm run dev
```

---

## 🔧 Prerequisites

- [ ] Python 3.8+ installed
- [ ] Node.js installed
- [ ] MongoDB installed or Atlas account

---

## 🎯 Quick Test

1. Backend: http://localhost:5000/api/health
2. Products: http://localhost:5000/api/products
3. Frontend: http://localhost:5173/

---

## 📝 Test Credentials

- john@example.com / password123
- jane@example.com / password123
- admin@example.com / admin123

---

## ⚠️ Common Issues

**Problem:** "No module named 'flask'"
**Solution:** Run `pip install Flask Flask-MongoEngine Flask-JWT-Extended Flask-CORS python-dotenv Werkzeug`

**Problem:** MongoDB connection error
**Solution:** Edit `backend\.env` with correct MongoDB URI

**Problem:** Import error with 'optional'
**Solution:** Fixed in code, no action needed

---

## 📚 More Documentation

- `SETUP_GUIDE.md` - Detailed setup instructions
- `TESTING_GUIDE.md` - Testing procedures
- `COMPLETE_SETUP_SUMMARY.md` - Full overview
- `backend/ARCHITECTURE.md` - Backend structure

---

## 🎉 Ready to Start?

**Just run:** `backend\setup-and-run.bat`

This will handle everything automatically!
