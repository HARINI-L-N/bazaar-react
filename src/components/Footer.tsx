import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-primary text-primary-foreground mt-auto">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">ShopHub</h3>
            <p className="text-sm text-primary-foreground/80">
              Your one-stop shop for everything you need.
            </p>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/" className="hover:text-accent transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/cart" className="hover:text-accent transition-colors">
                  Shopping Cart
                </Link>
              </li>
              <li>
                <Link to="/profile" className="hover:text-accent transition-colors">
                  My Account
                </Link>
              </li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4">Customer Service</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#" className="hover:text-accent transition-colors">
                  Help Center
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-accent transition-colors">
                  Returns
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-accent transition-colors">
                  Shipping Info
                </a>
              </li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4">About</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#" className="hover:text-accent transition-colors">
                  About Us
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-accent transition-colors">
                  Contact
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-accent transition-colors">
                  Privacy Policy
                </a>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-primary-foreground/20 mt-8 pt-8 text-center text-sm text-primary-foreground/80">
          <p>&copy; {new Date().getFullYear()} ShopHub. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
