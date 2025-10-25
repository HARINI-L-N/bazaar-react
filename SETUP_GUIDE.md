# Complete Setup Guide - Frontend + Backend

## 🎯 Goal
Set up MongoDB database and test both frontend and backend integration.

## 📋 Prerequisites Checklist
- [ ] Python 3.8+ installed
- [ ] Node.js installed (for React frontend)
- [ ] MongoDB installed or MongoDB Atlas account

---

## Step 1: Install MongoDB (Choose ONE Option)

### Option A: MongoDB Community Server (Local)

1. **Download MongoDB**
   - Visit: https://www.mongodb.com/try/download/community
   - Select Windows 64-bit
   - Download and install with default settings

2. **Verify Installation**
   ```powershell
   mongod --version
   ```

3. **Start MongoDB**
   - MongoDB runs as a Windows service automatically
   - Or manually: Open Services → Start "MongoDB" service

### Option B: MongoDB Atlas (Cloud - Recommended for Beginners)

1. **Create Free Account**
   - Visit: https://www.mongodb.com/atlas
   - Sign up for free account

2. **Create Free Cluster**
   - Click "Build a Database"
   - Choose FREE tier (M0)
   - Choose your preferred region
   - Click "Create"

3. **Get Connection String**
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)

---

## Step 2: Set Up Backend

### 2.1 Navigate to Backend Directory
```powershell
cd .\backend\
```

### 2.2 Create Virtual Environment
```powershell
python -m venv venv
```v

### 2.3 Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

**If you get an execution policy error, run:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2.4 Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2.5 Configure Environment Variables

Create a `.env` file in the backend directory:
```powershell
# Copy from template
copy env.example .env
```

Edit `.env` with your MongoDB connection:

**For Local MongoDB:**
```
MONGODB_URI=mongodb://localhost:27017/ecommerce_db
```

**For MongoDB Atlas:**
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/ecommerce_db
```

### 2.6 Populate Database with Sample Data
```powershell
python populate_db.py
```

**Expected Output:**
```
Sample data created successfully!
Users created: 3
Products created: 10
Test credentials:
- John Doe: john@example.com / password123
- Jane Smith: jane@example.com / password123
```

### 2.7 Start Backend Server
```powershell
python app.py
```

**Expected Output:**
```
 * Running on http://0.0.0.0:5000
```

**Test the backend in browser:** http://localhost:5000/api/health

---

## Step 3: Set Up Frontend

### 3.1 Navigate to Root Directory
```powershell
cd ..
```

### 3.2 Install Dependencies (if not already done)
```powershell
npm install
```

### 3.3 Update API Configuration

Create or update `.env` file in root directory:
```powershell
VITE_API_BASE_URL=http://localhost:5000/api
```

### 3.4 Start Frontend Server
```powershell
npm run dev
```

**Expected Output:**
```
  VITE v5.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

---

## Step 4: Test Integration

### 4.1 Test Backend API

Open browser and test these URLs:

✅ **Health Check:**
```
http://localhost:5000/api/health
```

✅ **Get Products:**
```
http://localhost:5000/api/products
```

✅ **Get Product Categories:**
```
http://localhost:5000/api/products/categories
```

### 4.2 Test Frontend-Backend Connection

1. Open frontend: http://localhost:5173/
2. Check browser console (F12) for any errors
3. Products should load from backend
4. Try logging in with test credentials

### 4.3 Test Full Flow

1. **Home Page** → Should show products from backend
2. **Product Details** → Click any product to view details
3. **Login** → Use: `john@example.com` / `password123`
4. **Add to Cart** → Add products and view cart
5. **Place Order** → Create an order
6. **View Orders** → Check order history

---

## Step 5: Troubleshooting

### Problem: MongoDB Connection Error

**Solution:**
- Check if MongoDB is running
- Verify connection string in `.env`
- For Atlas: Make sure IP whitelist includes `0.0.0.0/0` (all IPs)

### Problem: Backend Won't Start

**Solution:**
```powershell
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Problem: Frontend Can't Connect to Backend

**Solution:**
1. Check `.env` file has correct API URL
2. Check CORS is enabled in backend
3. Check browser console for specific errors
4. Verify backend is running on port 5000

### Problem: Database Empty

**Solution:**
```powershell
cd backend
python populate_db.py
```

---

## Step 6: Verify Everything Works

### ✅ Backend Tests
```powershell
cd backend
python test_api.py
```

### ✅ Manual Checks

**Backend:**
- [ ] API responds at http://localhost:5000/api/health
- [ ] Products endpoint returns data
- [ ] Login endpoint works with test credentials

**Frontend:**
- [ ] Pages load without errors
- [ ] Products display from backend
- [ ] Login functionality works
- [ ] Cart functionality works
- [ ] Orders can be created

---

## 🎉 Success Indicators

You'll know everything is working when:

1. ✅ Backend runs on http://localhost:5000
2. ✅ Frontend runs on http://localhost:5173
3. ✅ Products appear on frontend from backend
4. ✅ Login works with test credentials
5. ✅ Can add items to cart
6. ✅ Can create orders
7. ✅ No console errors in browser

---

## 🆘 Need Help?

If you encounter issues:

1. Check the error messages in terminal/console
2. Verify MongoDB is running
3. Check `.env` files are configured correctly
4. Ensure both servers are running
5. Check firewall settings

---

## 📝 Test Credentials

- **John Doe:** john@example.com / password123
- **Jane Smith:** jane@example.com / password123
- **Admin:** admin@example.com / admin123

---

## 🚀 Quick Commands Reference

```powershell
# Start Backend
cd backend
.\venv\Scripts\Activate.ps1
python app.py

# Start Frontend (in new terminal)
npm run dev

# Populate Database
cd backend
python populate_db.py

# Test API
cd backend
python test_api.py
```
