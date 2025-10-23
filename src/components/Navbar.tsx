import { Link } from 'react-router-dom';
import { ShoppingCart, User, Search, Menu } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { useCart } from '@/contexts/CartContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useState } from 'react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { cartCount } = useCart();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 bg-primary text-primary-foreground shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="text-2xl font-bold">ShopHub</div>
          </Link>

          {/* Search Bar - Hidden on mobile */}
          <div className="hidden md:flex flex-1 max-w-2xl mx-8">
            <div className="relative w-full">
              <Input
                type="text"
                placeholder="Search products..."
                className="w-full pl-4 pr-12 bg-white text-foreground"
              />
              <Button
                size="sm"
                className="absolute right-0 top-0 h-full bg-accent hover:bg-accent/90"
              >
                <Search className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Right side buttons */}
          <div className="flex items-center space-x-4">
            {/* Mobile menu button */}
            <Button
              variant="ghost"
              size="sm"
              className="md:hidden text-primary-foreground"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              <Menu className="h-5 w-5" />
            </Button>

            {/* Desktop navigation */}
            <div className="hidden md:flex items-center space-x-4">
              {user ? (
                <>
                  <Link to="/profile">
                    <Button variant="ghost" size="sm" className="text-primary-foreground hover:text-primary-foreground/80">
                      <User className="h-5 w-5 mr-2" />
                      {user.name}
                    </Button>
                  </Link>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={logout}
                    className="text-primary-foreground hover:text-primary-foreground/80"
                  >
                    Logout
                  </Button>
                </>
              ) : (
                <Link to="/login">
                  <Button variant="ghost" size="sm" className="text-primary-foreground hover:text-primary-foreground/80">
                    <User className="h-5 w-5 mr-2" />
                    Sign In
                  </Button>
                </Link>
              )}

              <Link to="/cart">
                <Button variant="ghost" size="sm" className="relative text-primary-foreground hover:text-primary-foreground/80">
                  <ShoppingCart className="h-5 w-5" />
                  {cartCount > 0 && (
                    <span className="absolute -top-1 -right-1 bg-accent text-accent-foreground text-xs rounded-full h-5 w-5 flex items-center justify-center font-bold">
                      {cartCount}
                    </span>
                  )}
                </Button>
              </Link>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden pb-4 space-y-2">
            <div className="relative mb-4">
              <Input
                type="text"
                placeholder="Search products..."
                className="w-full pl-4 pr-12 bg-white text-foreground"
              />
              <Button
                size="sm"
                className="absolute right-0 top-0 h-full bg-accent hover:bg-accent/90"
              >
                <Search className="h-4 w-4" />
              </Button>
            </div>
            {user ? (
              <>
                <Link to="/profile" className="block">
                  <Button variant="ghost" className="w-full justify-start text-primary-foreground">
                    <User className="h-5 w-5 mr-2" />
                    Profile
                  </Button>
                </Link>
                <Button
                  variant="ghost"
                  onClick={logout}
                  className="w-full justify-start text-primary-foreground"
                >
                  Logout
                </Button>
              </>
            ) : (
              <Link to="/login" className="block">
                <Button variant="ghost" className="w-full justify-start text-primary-foreground">
                  <User className="h-5 w-5 mr-2" />
                  Sign In
                </Button>
              </Link>
            )}
            <Link to="/cart" className="block">
              <Button variant="ghost" className="w-full justify-start text-primary-foreground">
                <ShoppingCart className="h-5 w-5 mr-2" />
                Cart ({cartCount})
              </Button>
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
