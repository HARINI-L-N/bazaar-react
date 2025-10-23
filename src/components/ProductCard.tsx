import { Link, useNavigate } from 'react-router-dom';
import { Star, ShoppingCart, Heart } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { useCart } from '@/contexts/CartContext';
import { useWishlist } from '@/contexts/WishlistContext';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from 'sonner';

interface ProductCardProps {
  id: string;
  title: string;
  price: number;
  image: string;
  rating: number;
  reviews: number;
}

const ProductCard = ({ id, title, price, image, rating, reviews }: ProductCardProps) => {
  const { addToCart } = useCart();
  const { addToWishlist, removeFromWishlist, isInWishlist } = useWishlist();
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    if (!user) {
      toast.error('Please sign in to add items to your cart', {
        action: {
          label: 'Sign In',
          onClick: () => navigate('/login'),
        },
      });
      return;
    }
    addToCart({ id, title, price, image });
    toast.success('Added to cart!');
  };

  const handleWishlistToggle = (e: React.MouseEvent) => {
    e.preventDefault();
    if (!user) {
      toast.error('Please sign in to save items to your wishlist', {
        action: {
          label: 'Sign In',
          onClick: () => navigate('/login'),
        },
      });
      return;
    }
    if (isInWishlist(id)) {
      removeFromWishlist(id);
      toast.success('Removed from wishlist');
    } else {
      addToWishlist({ id, title, price, image, rating });
      toast.success('Added to wishlist!');
    }
  };

  return (
    <Link to={`/product/${id}`}>
      <Card className="h-full hover:shadow-[var(--shadow-hover)] transition-all duration-300 hover:-translate-y-1 bg-card border-border">
        <CardContent className="p-4">
          <div className="relative aspect-square mb-4 overflow-hidden rounded-lg bg-muted">
            <img
              src={image}
              alt={title}
              className="w-full h-full object-cover transition-transform duration-300 hover:scale-110"
            />
            <Button
              variant="ghost"
              size="sm"
              onClick={handleWishlistToggle}
              className="absolute top-2 right-2 bg-background/80 hover:bg-background backdrop-blur-sm"
            >
              <Heart
                className={`h-5 w-5 ${
                  isInWishlist(id)
                    ? 'fill-accent text-accent'
                    : 'text-muted-foreground'
                }`}
              />
            </Button>
          </div>
          
          <h3 className="font-semibold text-card-foreground line-clamp-2 mb-2 min-h-[2.5rem]">
            {title}
          </h3>
          
          <div className="flex items-center mb-2">
            <div className="flex items-center">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={`h-4 w-4 ${
                    i < Math.floor(rating)
                      ? 'fill-accent text-accent'
                      : 'text-muted-foreground/30'
                  }`}
                />
              ))}
            </div>
            <span className="text-sm text-muted-foreground ml-2">
              ({reviews})
            </span>
          </div>
          
          <div className="text-2xl font-bold text-card-foreground">
            ${price.toFixed(2)}
          </div>
        </CardContent>
        
        <CardFooter className="p-4 pt-0">
          <Button
            onClick={handleAddToCart}
            className="w-full bg-accent hover:bg-accent/90 text-accent-foreground"
          >
            <ShoppingCart className="h-4 w-4 mr-2" />
            Add to Cart
          </Button>
        </CardFooter>
      </Card>
    </Link>
  );
};

export default ProductCard;
