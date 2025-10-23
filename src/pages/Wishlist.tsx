import { Link } from 'react-router-dom';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { useWishlist } from '@/contexts/WishlistContext';
import { useCart } from '@/contexts/CartContext';
import { Heart, ShoppingCart, Trash2 } from 'lucide-react';
import { toast } from 'sonner';

const Wishlist = () => {
  const { wishlist, removeFromWishlist } = useWishlist();
  const { addToCart } = useCart();

  const handleAddToCart = (item: any) => {
    addToCart({ id: item.id, title: item.title, price: item.price, image: item.image });
    toast.success('Added to cart!');
  };

  const handleRemove = (id: string) => {
    removeFromWishlist(id);
    toast.success('Removed from wishlist');
  };

  if (wishlist.length === 0) {
    return (
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-1 container mx-auto px-4 py-16">
          <div className="text-center">
            <Heart className="h-24 w-24 mx-auto mb-4 text-muted-foreground/50" />
            <h2 className="text-3xl font-bold mb-4 text-foreground">Your wishlist is empty</h2>
            <p className="text-muted-foreground mb-8">
              Save your favorite items for later!
            </p>
            <Link to="/">
              <Button className="bg-accent hover:bg-accent/90 text-accent-foreground">
                Browse Products
              </Button>
            </Link>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      
      <main className="flex-1 container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-2 text-foreground">My Wishlist</h1>
        <p className="text-muted-foreground mb-8">{wishlist.length} items saved</p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {wishlist.map((item) => (
            <Card key={item.id} className="shadow-[var(--shadow-elegant)]">
              <CardContent className="p-4">
                <Link to={`/product/${item.id}`}>
                  <div className="aspect-square mb-4 overflow-hidden rounded-lg bg-muted">
                    <img
                      src={item.image}
                      alt={item.title}
                      className="w-full h-full object-cover hover:scale-110 transition-transform duration-300"
                    />
                  </div>
                </Link>
                
                <Link to={`/product/${item.id}`}>
                  <h3 className="font-semibold text-foreground line-clamp-2 mb-2 hover:text-accent transition-colors">
                    {item.title}
                  </h3>
                </Link>
                
                <div className="text-2xl font-bold text-foreground mb-4">
                  ${item.price.toFixed(2)}
                </div>
                
                <div className="flex gap-2">
                  <Button
                    onClick={() => handleAddToCart(item)}
                    className="flex-1 bg-accent hover:bg-accent/90 text-accent-foreground"
                  >
                    <ShoppingCart className="h-4 w-4 mr-2" />
                    Add to Cart
                  </Button>
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={() => handleRemove(item.id)}
                    className="text-destructive hover:text-destructive border-destructive/30 hover:border-destructive"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Wishlist;
