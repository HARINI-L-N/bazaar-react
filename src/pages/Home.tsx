import { useEffect, useState } from 'react';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ProductList from '@/components/ProductList';
import { mockProducts } from '@/lib/mockData';
import heroBanner from '@/assets/hero-banner.jpg';

const Home = () => {
  const [products, setProducts] = useState(mockProducts);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // TODO: Replace with actual API call
    // endpoints.getProducts().then(response => setProducts(response.data));
    setIsLoading(false);
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      
      <main className="flex-1">
        {/* Hero Section */}
        <div 
          className="relative h-[400px] md:h-[500px] bg-cover bg-center"
          style={{ backgroundImage: `url(${heroBanner})` }}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-primary/90 to-primary/60" />
          <div className="relative container mx-auto px-4 h-full flex items-center">
            <div className="text-primary-foreground max-w-2xl">
              <h1 className="text-4xl md:text-6xl font-bold mb-4 animate-fade-in">
                Welcome to ShopHub
              </h1>
              <p className="text-xl md:text-2xl mb-8 animate-fade-in">
                Discover amazing products at unbeatable prices
              </p>
            </div>
          </div>
        </div>

        {/* Products Section */}
        <div className="container mx-auto px-4 py-12">
          {isLoading ? (
            <div className="text-center py-20">
              <div className="text-xl">Loading products...</div>
            </div>
          ) : (
            <ProductList products={products} title="Featured Products" />
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Home;
