import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ProductList from '@/components/ProductList';
import { Button } from '@/components/ui/button';
import { Star, ShoppingCart, Heart, Plus, Minus } from 'lucide-react';
import { endpoints } from '@/lib/api';
import { useCart } from '@/contexts/CartContext';
import { useWishlist } from '@/contexts/WishlistContext';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from 'sonner';

const ProductDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState<any | null>(null);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [quantity, setQuantity] = useState(1);
  const { addToCart } = useCart();
  const { addToWishlist, removeFromWishlist, isInWishlist } = useWishlist();
  const { user } = useAuth();

  useEffect(() => {
    if (!id) return;
    endpoints
      .getProduct(id)
      .then((res) => {
        const payload = res.data && res.data.data ? res.data.data : res.data;
        const p = payload || null;
        if (!p) {
          setProduct(null);
          return;
        }

        const transformed = {
          id: p.id || p._id || String(p.id),
          title: p.title || p.name || '',
          price: p.price ?? p.amount ?? 0,
          image: p.image || p.image_url || p.imageUrl || '',
          rating: p.rating ?? 0,
          reviews: p.review_count ?? p.reviews ?? 0,
          description: p.description || '',
          category: p.category || '',
          inStock: (p.stock_quantity ?? p.stock ?? 0) > 0,
        };

        setProduct(transformed);
      })
      .catch((err) => console.error('Failed to load product', err));

    // Load product-level content recommendations (no auth required)
    endpoints
      .getProductRecommendations(id)
      .then((res) => {
        const payload = res.data && res.data.data ? res.data.data : res.data;
        const rawRecommendations = payload?.recommendations || [];
        const transform = (item) => {
          const p = item.product || item;
          return {
            id: p.id || p._id || String(p.id),
            title: p.title || p.name || '',
            price: p.price ?? p.amount ?? 0,
            image: p.image || p.image_url || p.imageUrl || '',
            rating: p.rating ?? 0,
            reviews: p.review_count ?? p.reviews ?? 0,
            description: p.description || '',
            category: p.category || '',
            inStock: (p.stock_quantity ?? p.stock ?? 0) > 0,
          };
        };
        setRecommendations(Array.isArray(rawRecommendations) ? rawRecommendations.map(transform) : []);
      })
      .catch((err) => console.error('Failed to load recommendations', err));
  }, [id]);

  if (!product) {
    return (
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-xl">Product not found</div>
        </div>
        <Footer />
      </div>
    );
  }

  const handleAddToCart = () => {
    if (!user) {
      toast.error('Please sign in to add items to your cart', {
        action: {
          label: 'Sign In',
          onClick: () => navigate('/login'),
        },
      });
      return;
    }
    for (let i = 0; i < quantity; i++) {
      addToCart({
        id: product.id,
        title: product.title,
        price: product.price,
        image: product.image,
      });
    }
    toast.success(`Added ${quantity} item(s) to cart!`);
    setQuantity(1);
  };

  const handleWishlistToggle = () => {
    if (!user) {
      toast.error('Please sign in to save items to your wishlist', {
        action: {
          label: 'Sign In',
          onClick: () => navigate('/login'),
        },
      });
      return;
    }
    if (isInWishlist(product.id)) {
      removeFromWishlist(product.id);
      toast.success('Removed from wishlist');
    } else {
      addToWishlist({
        id: product.id,
        title: product.title,
        price: product.price,
        image: product.image,
        rating: product.rating,
      });
      toast.success('Added to wishlist!');
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      
      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
          {/* Product Image */}
          <div className="aspect-square rounded-lg overflow-hidden bg-muted shadow-[var(--shadow-elegant)]">
            <img
              src={product.image}
              alt={product.title}
              className="w-full h-full object-cover"
            />
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold mb-2 text-foreground">
                {product.title}
              </h1>
              <div className="flex items-center mb-4">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className={`h-5 w-5 ${
                        i < Math.floor(product.rating)
                          ? 'fill-accent text-accent'
                          : 'text-muted-foreground/30'
                      }`}
                    />
                  ))}
                </div>
                <span className="ml-2 text-muted-foreground">
                  {product.rating} ({product.reviews} reviews)
                </span>
              </div>
            </div>

            <div className="text-4xl font-bold text-foreground">
              ${product.price.toFixed(2)}
            </div>

            <div className="py-4 border-t border-b border-border">
              <p className="text-lg text-foreground/80">
                {product.description}
              </p>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Category:</span>
                <span className="font-semibold text-foreground">{product.category}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Availability:</span>
                <span className="font-semibold text-accent">
                  {product.inStock ? 'In Stock' : 'Out of Stock'}
                </span>
              </div>
            </div>

            {/* Quantity Selector */}
            <div className="flex items-center gap-4">
              <span className="text-sm text-muted-foreground">Quantity:</span>
              <div className="flex items-center border border-border rounded-lg">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  disabled={quantity <= 1}
                >
                  <Minus className="h-4 w-4" />
                </Button>
                <span className="px-6 font-semibold text-foreground">{quantity}</span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setQuantity(Math.min(10, quantity + 1))}
                  disabled={quantity >= 10}
                >
                  <Plus className="h-4 w-4" />
                </Button>
              </div>
            </div>

            <div className="flex gap-3">
              <Button
                onClick={handleAddToCart}
                size="lg"
                disabled={!product.inStock}
                className="flex-1 bg-accent hover:bg-accent/90 text-accent-foreground text-lg"
              >
                <ShoppingCart className="h-5 w-5 mr-2" />
                Add to Cart
              </Button>
              <Button
                onClick={handleWishlistToggle}
                variant="outline"
                size="lg"
                className="border-2"
              >
                <Heart
                  className={`h-5 w-5 ${
                    isInWishlist(product.id)
                      ? 'fill-accent text-accent'
                      : ''
                  }`}
                />
              </Button>
            </div>
          </div>
        </div>

        {/* Recommendations */}
        <div className="border-t border-border pt-12">
          <ProductList products={recommendations} title="You May Also Like" />
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default ProductDetails;
