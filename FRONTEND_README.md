# ShopHub - E-Commerce Frontend

A complete Amazon-inspired e-commerce frontend built with React, TypeScript, and Tailwind CSS. This application is ready to integrate with a Flask + MongoDB backend.

## 🚀 Features

- **Home Page**: Grid layout with featured products, hero section, and responsive design
- **Product Search**: Real-time search with filter and sort capabilities
- **Product Details**: Full product information with recommendations, quantity selector, and wishlist
- **Authentication**: Login and registration with form validation and auto-redirect
- **User Profile**: Display user details, order history, and recently viewed products
- **Shopping Cart**: Full cart management (login required) with quantity updates and order summary
- **Wishlist**: Save favorite products for later (login required)
- **Protected Routes**: Authentication-based route protection
- **Loading States**: Professional skeleton loaders for better UX
- **Responsive Design**: Mobile-first design that works on all devices
- **State Management**: Context API for auth, cart, and wishlist with localStorage persistence
- **Professional UX**: Toast notifications, empty states, and smooth animations

## 🛠️ Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client
- **Shadcn/ui** - UI components
- **Context API** - State management
- **Vite** - Build tool

## ✨ Professional Features

### Authentication-Required Cart
- Users must sign in to add items to cart
- Friendly prompts with quick sign-in actions
- Cart data persists per user account

### Wishlist System
- Save favorite products for later
- Heart icon on product cards for quick wishlist access
- Protected route requiring authentication
- Separate wishlist counter in navigation

### Advanced Search & Filtering
- Real-time product search
- Category filtering
- Multiple sort options (price, rating, featured)
- Search results with product count
- URL-based search queries

### Professional UI/UX
- Loading skeleton screens
- Quantity selector on product details
- Empty state designs for cart and wishlist
- Interactive toast notifications with actions
- Smooth hover animations and transitions
- Responsive mobile navigation

## 📦 Installation

### Prerequisites
- Node.js 18+ and npm

### Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file in the root directory:
```env
VITE_API_BASE_URL=http://localhost:5000
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:8080`

## 🔌 Backend Integration

The frontend is pre-configured to connect to your Flask + MongoDB backend. API endpoints are defined in `src/lib/api.ts`.

### Expected Backend Endpoints

#### Products
- `GET /products` - Fetch all products
- `GET /products/:id` - Fetch single product
- `GET /recommendations/:id` - Get product recommendations

#### Authentication
- `POST /users/register` - Register new user
  ```json
  { "email": "string", "password": "string", "name": "string" }
  ```
- `POST /users/login` - Login user
  ```json
  { "email": "string", "password": "string" }
  ```

#### User Data
- `GET /users/:id/history` - Get user's viewed products
- `GET /users/:id/orders` - Get user's orders

#### Cart
- `GET /cart` - Get user's cart
- `POST /cart` - Add item to cart
  ```json
  { "productId": "string", "quantity": number }
  ```
- `PUT /cart/:itemId` - Update cart item quantity
- `DELETE /cart/:itemId` - Remove item from cart

#### Orders
- `GET /orders` - Get user's orders
- `POST /orders` - Create new order
  ```json
  { "items": [], "total": number }
  ```

### Connecting to Your Backend

1. Update the `VITE_API_BASE_URL` in your `.env` file to point to your Flask backend
2. Uncomment the API calls in the page components (they're marked with `// TODO:`)
3. The authentication token is automatically added to requests via Axios interceptors

Example integration in a component:
```typescript
import { endpoints } from '@/lib/api';

// In your component
useEffect(() => {
  endpoints.getProducts()
    .then(response => setProducts(response.data))
    .catch(error => console.error('Error fetching products:', error));
}, []);
```

## 📁 Project Structure

```
src/
├── assets/           # Images and static files
├── components/       # Reusable components
│   ├── ui/          # Shadcn UI components
│   ├── Navbar.tsx
│   ├── Footer.tsx
│   ├── ProductCard.tsx
│   ├── ProductCardSkeleton.tsx
│   ├── ProductList.tsx
│   └── ProtectedRoute.tsx
├── contexts/        # React Context providers
│   ├── AuthContext.tsx
│   ├── CartContext.tsx
│   └── WishlistContext.tsx
├── lib/            # Utilities and API config
│   ├── api.ts      # Axios configuration
│   ├── utils.ts    # Helper functions
│   └── mockData.ts # Mock data for development
├── pages/          # Page components
│   ├── Home.tsx
│   ├── ProductDetails.tsx
│   ├── Login.tsx
│   ├── Register.tsx
│   ├── Profile.tsx
│   ├── Wishlist.tsx
│   └── Cart.tsx
├── App.tsx         # Main app component with routing
└── index.css       # Global styles and design system
```

## 🎨 Design System

The application uses a carefully crafted design system inspired by Amazon:

- **Primary Color**: Deep navy/indigo (#1a2942)
- **Accent Color**: Warm orange (#f97316)
- **Background**: Clean whites and light grays
- **Typography**: System fonts with bold headings
- **Shadows**: Elegant depth with subtle shadows
- **Animations**: Smooth transitions on hover and interactions

All design tokens are defined in `src/index.css` and can be customized.

## 🔒 Authentication Flow

1. User registers via `/register` page
2. Credentials are sent to backend `/users/register`
3. User logs in via `/login` page
4. Token is stored in localStorage
5. Protected routes check for authentication
6. Token is automatically added to API requests
7. **Cart and wishlist require authentication**
8. Automatic redirect when already logged in

## 🛒 Shopping Cart Flow

1. User must be logged in to add products to cart
2. If not logged in, user sees toast with "Sign In" action
3. Cart state is managed via CartContext
4. Cart persists in localStorage per user account
5. User can update quantities or remove items
6. Checkout creates an order via `/orders` endpoint

## ❤️ Wishlist Flow

1. User must be logged in to add to wishlist
2. Heart icon on product cards for quick access
3. Wishlist state managed via WishlistContext
4. Data persists in localStorage per user
5. Can move items from wishlist to cart
6. Dedicated `/wishlist` page (protected route)

## 📱 Responsive Design

The application is built mobile-first with breakpoints:
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## 🧪 Mock Data

For development without a backend, mock data is provided in `src/lib/mockData.ts`. This includes:
- Sample products
- Order history
- View history

## 🚀 Building for Production

```bash
npm run build
```

The production build will be in the `dist/` folder.

## 🔧 Environment Variables

- `VITE_API_BASE_URL` - Backend API URL (default: http://localhost:5000)

## 📝 Next Steps

1. Start your Flask + MongoDB backend
2. Update the API base URL in `.env`
3. Test the authentication flow
4. Implement the remaining backend endpoints
5. Replace mock data with real API calls
6. Add error handling and loading states
7. Implement search functionality
8. Add filters and sorting for products

## 🤝 Integration Checklist

- [ ] Flask backend running
- [ ] MongoDB connected
- [ ] CORS enabled on backend
- [ ] API endpoints implemented
- [ ] Environment variables configured
- [ ] Authentication tested
- [ ] Products loading from API
- [ ] Cart functionality working
- [ ] Orders being created

## 📄 License

MIT
