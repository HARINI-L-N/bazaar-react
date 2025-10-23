import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ProductList from '@/components/ProductList';
import { Button } from '@/components/ui/button';
import { Star, ShoppingCart } from 'lucide-react';
import { mockProducts } from '@/lib/mockData';
import { useCart } from '@/contexts/CartContext';
import { toast } from 'sonner';

const ProductDetails = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(mockProducts.find(p => p.id === id));
  const [recommendations, setRecommendations] = useState(mockProducts.slice(0, 4));
  const { addToCart } = useCart();

  useEffect(() => {
    // TODO: Replace with actual API calls
    // endpoints.getProduct(id).then(response => setProduct(response.data));
    // endpoints.getRecommendations(id).then(response => setRecommendations(response.data));
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
    addToCart({
      id: product.id,
      title: product.title,
      price: product.price,
      image: product.image,
    });
    toast.success('Added to cart!');
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

            <Button
              onClick={handleAddToCart}
              size="lg"
              className="w-full bg-accent hover:bg-accent/90 text-accent-foreground text-lg"
            >
              <ShoppingCart className="h-5 w-5 mr-2" />
              Add to Cart
            </Button>
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
