import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ProductList from '@/components/ProductList';
import ProductCardSkeleton from '@/components/ProductCardSkeleton';
import { endpoints } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import heroBanner from '@/assets/hero-banner.jpg';
import { SlidersHorizontal } from 'lucide-react';

const Home = () => {
  const [searchParams] = useSearchParams();
  const [products, setProducts] = useState<any[]>([]);
  const [filteredProducts, setFilteredProducts] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [sortBy, setSortBy] = useState('featured');
  const [filterCategory, setFilterCategory] = useState('all');

  const searchQuery = searchParams.get('search');

  useEffect(() => {
    // Load products from backend
    setIsLoading(true);
    endpoints
      .getProducts()
      .then((res) => {
        // API responses are wrapped as { data: <payload>, message: ... }
        const payload = res.data && res.data.data ? res.data.data : res.data;
        const rawProducts = payload?.products || [];

        // Normalize backend product shape to frontend-friendly shape used throughout the UI
  const transform = (p) => ({
          id: p.id || p._id || (p._id && p._id.$oid) || String(p.id),
          title: p.title || p.name || '',
          price: p.price ?? p.amount ?? 0,
          image: p.image || p.image_url || p.imageUrl || '',
          rating: p.rating ?? 0,
          reviews: p.review_count ?? p.reviews ?? 0,
          description: p.description || p.desc || '',
          category: p.category || (p.category && String(p.category)) || '',
          inStock: (p.stock_quantity ?? p.stock ?? 0) > 0,
        });

        setProducts(Array.isArray(rawProducts) ? rawProducts.map(transform) : []);
      })
      .catch((err) => {
        console.error('Failed to load products', err);
        setProducts([]);
      })
      .finally(() => setIsLoading(false));
  }, []);

  useEffect(() => {
    let filtered = [...products];

    // Apply search filter
    if (searchQuery) {
      filtered = filtered.filter(product =>
        product.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        product.category.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Apply category filter
    if (filterCategory !== 'all') {
      filtered = filtered.filter(product => product.category === filterCategory);
    }

    // Apply sorting
    switch (sortBy) {
      case 'price-low':
        filtered.sort((a, b) => a.price - b.price);
        break;
      case 'price-high':
        filtered.sort((a, b) => b.price - a.price);
        break;
      case 'rating':
        filtered.sort((a, b) => b.rating - a.rating);
        break;
      case 'featured':
      default:
        // Keep original order
        break;
    }

    setFilteredProducts(filtered);
  }, [products, searchQuery, sortBy, filterCategory]);

  const categories = ['all', ...Array.from(new Set(products.map(p => p.category)))] as string[];

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
          {/* Search Results Header */}
          {searchQuery && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-foreground">
                Search results for "{searchQuery}"
              </h2>
              <p className="text-muted-foreground">
                {filteredProducts.length} products found
              </p>
            </div>
          )}

          {/* Filters and Sort */}
          <div className="flex flex-col md:flex-row gap-4 mb-8">
            <div className="flex items-center gap-2 flex-1">
              <SlidersHorizontal className="h-5 w-5 text-muted-foreground" />
              <Select value={filterCategory} onValueChange={setFilterCategory}>
                <SelectTrigger className="w-full md:w-48">
                  <SelectValue placeholder="Category" />
                </SelectTrigger>
                <SelectContent>
                  {categories.map(category => (
                    <SelectItem key={category} value={category}>
                      {category.charAt(0).toUpperCase() + category.slice(1)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-full md:w-48">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="featured">Featured</SelectItem>
                <SelectItem value="price-low">Price: Low to High</SelectItem>
                <SelectItem value="price-high">Price: High to Low</SelectItem>
                <SelectItem value="rating">Highest Rated</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {isLoading ? (
            <div>
              <h2 className="text-3xl font-bold mb-6 text-foreground">Featured Products</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {[...Array(8)].map((_, i) => (
                  <ProductCardSkeleton key={i} />
                ))}
              </div>
            </div>
          ) : filteredProducts.length === 0 ? (
            <div className="text-center py-20">
              <h3 className="text-2xl font-bold mb-2 text-foreground">No products found</h3>
              <p className="text-muted-foreground mb-6">Try adjusting your filters or search terms</p>
              <Button
                onClick={() => {
                  setFilterCategory('all');
                  setSortBy('featured');
                }}
                variant="outline"
              >
                Clear Filters
              </Button>
            </div>
          ) : (
            <ProductList 
              products={filteredProducts} 
              title={!searchQuery ? "Featured Products" : undefined} 
            />
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Home;
