# Testing Guide - Frontend + Backend Integration

## 🧪 How to Test if Everything Works

### Prerequisites
- MongoDB running (local or Atlas)
- Backend server running on port 5000
- Frontend server running on port 5173

---

## Step 1: Test Backend API Directly

### 1.1 Health Check
Open browser: http://localhost:5000/api/health

**Expected Response:**
```json
{
  "status": "OK",
  "message": "E-commerce API is running"
}
```

✅ **Status:** Working if you see this message

---

### 1.2 Get Products (No Auth Required)
Open browser: http://localhost:5000/api/products

**Expected Response:**
```json
{
  "data": {
    "products": [
      {
        "id": "...",
        "name": "Wireless Bluetooth Headphones",
        "price": 199.99,
        ...
      }
    ],
    "pagination": {...}
  }
}
```

✅ **Status:** Working if you see product list

---

### 1.3 Get Categories
Open browser: http://localhost:5000/api/products/categories

**Expected Response:**
```json
{
  "data": ["Electronics", "Clothing", "Home & Kitchen", ...]
}
```

✅ **Status:** Working if you see categories

---

### 1.4 Test Login
Use any REST client (Postman, Insomnia, or browser console):

**Request:**
```javascript
fetch('http://localhost:5000/api/users/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    username: 'john@example.com',
    password: 'password123'
  })
})
.then(r => r.json())
.then(console.log)
```

**Expected Response:**
```json
{
  "data": {
    "user": {...},
    "access_token": "eyJ..."
  },
  "message": "Login successful"
}
```

✅ **Status:** Working if you get access_token

---

## Step 2: Test Frontend

### 2.1 Open Frontend
Browser: http://localhost:5173/

### 2.2 Check Browser Console
Press F12 → Console tab

✅ **Status:** No errors = Working
❌ **Status:** Errors = Check API connection

---

### 2.3 Test Product Loading
Go to Home page

**Expected Behavior:**
- Products display from backend
- Product cards show name, price, etc.
- No loading spinners stuck

✅ **Status:** Products visible = Working

---

### 2.4 Test Product Details
Click any product

**Expected Behavior:**
- Product details page loads
- Shows full product information
- Related products appear

✅ **Status:** Details load = Working

---

## Step 3: Test Authentication Flow

### 3.1 Register New User
1. Go to Register page
2. Fill in details:
   - Username: testuser
   - Email: test@example.com
   - Password: testpass123
3. Click Register

**Expected Behavior:**
- Redirects to login or home
- User is logged in
- No error messages

✅ **Status:** Can register = Working

---

### 3.2 Login with Test Credentials
1. Go to Login page
2. Enter: john@example.com / password123
3. Click Login

**Expected Behavior:**
- Redirects to home
- User info appears in navbar
- Login button changes to user menu

✅ **Status:** Can login = Working

---

### 3.3 Logout
Click Logout button

**Expected Behavior:**
- Redirects to home
- User menu disappears
- Login button appears

✅ **Status:** Can logout = Working

---

## Step 4: Test Shopping Features

### 4.1 Add to Cart
1. Browse products
2. Click "Add to Cart"
3. Go to Cart page

**Expected Behavior:**
- Product appears in cart
- Correct quantity shown
- Total calculated correctly

✅ **Status:** Can add items = Working

---

### 4.2 Update Cart Quantity
1. In cart, change quantity
2. Item updates

**Expected Behavior:**
- Quantity changes
- Total updates
- No errors

✅ **Status:** Can update = Working

---

### 4.3 Remove from Cart
1. Click remove button
2. Item disappears

**Expected Behavior:**
- Item removed
- Cart updates
- Total recalculates

✅ **Status:** Can remove = Working

---

## Step 5: Test Orders

### 5.1 Create Order
1. Add items to cart
2. Click "Checkout"
3. Fill shipping address
4. Submit order

**Expected Behavior:**
- Order created successfully
- Cart clears
- Redirects to order confirmation

✅ **Status:** Can create order = Working

---

### 5.2 View Order History
1. Go to Profile or Orders page
2. View past orders

**Expected Behavior:**
- Orders list displays
- Order details visible
- Status shown

✅ **Status:** Can view orders = Working

---

## Step 6: Test Recommendations

### 6.1 View Recommendations
1. Login as a user
2. Browse some products
3. Go to recommendations page (if exists)

**Expected Behavior:**
- Personalized products shown
- Based on viewing history
- Products appear relevant

✅ **Status:** Recommendations show = Working

---

## Step 7: Complete Integration Test

### Full User Journey Test

1. **Browse as Guest**
   - ✅ View products
   - ✅ See product details
   - ❌ Cannot add to cart (should redirect to login)

2. **Register & Login**
   - ✅ Register new account
   - ✅ Login successfully
   - ✅ User data persists

3. **Shop**
   - ✅ Browse products
   - ✅ Add items to cart
   - ✅ Update quantities
   - ✅ Remove items

4. **Checkout**
   - ✅ View cart summary
   - ✅ Fill shipping details
   - ✅ Create order
   - ✅ View order confirmation

5. **Order Management**
   - ✅ View order history
   - ✅ See order details
   - ✅ Track order status

---

## Common Issues & Solutions

### Issue: "Cannot connect to backend"
**Solution:**
- Check backend is running on port 5000
- Check `.env` has correct `VITE_API_BASE_URL`
- Check CORS is enabled in backend

### Issue: "Products not loading"
**Solution:**
- Open backend URL directly: http://localhost:5000/api/products
- Check browser console for specific errors
- Verify database has data (run populate_db.py)

### Issue: "Login doesn't work"
**Solution:**
- Check API endpoint matches backend
- Verify JWT token is stored in localStorage
- Check Authorization header is sent

### Issue: "Cart empty after page refresh"
**Solution:**
- Normal behavior if not persisted
- Check if cart endpoint returns data
- Verify user is logged in

### Issue: "Orders not saving"
**Solution:**
- Check backend orders endpoint
- Verify user authentication
- Check order data format matches backend

---

## Quick Test Checklist

Run through this checklist to verify everything:

**Backend Tests:**
- [ ] Health check works
- [ ] Products API returns data
- [ ] Categories API works
- [ ] Login returns JWT token
- [ ] Protected routes require auth

**Frontend Tests:**
- [ ] Pages load without errors
- [ ] Products display from backend
- [ ] Login/Register works
- [ ] Cart functionality works
- [ ] Orders can be created
- [ ] User data persists

**Integration Tests:**
- [ ] Frontend communicates with backend
- [ ] Authentication flow works
- [ ] Protected routes work
- [ ] Error handling works
- [ ] Loading states work

---

## Success Indicators

✅ **Everything Works When:**
1. Backend API responds correctly
2. Frontend loads without console errors
3. Products display from backend database
4. Users can register and login
5. Cart functionality works end-to-end
6. Orders can be created and viewed
7. No CORS errors in console
8. No network errors in browser DevTools

---

## Debugging Tips

### Check Browser DevTools
1. **Console Tab:** Look for JavaScript errors
2. **Network Tab:** Check API calls and responses
3. **Application Tab:** Check localStorage for tokens

### Check Backend Logs
- Look at terminal running Flask
- Check for error messages
- Verify database connections

### Check MongoDB
- Verify MongoDB is running
- Check database has collections
- Verify sample data exists

---

## Need Help?

If tests fail:
1. Check error messages in browser console
2. Check error messages in backend terminal
3. Verify all services are running
4. Check `.env` files are configured
5. Verify MongoDB connection

---

## Test Credentials

Use these to test:

- **John Doe:** john@example.com / password123
- **Jane Smith:** jane@example.com / password123
- **Admin:** admin@example.com / admin123
