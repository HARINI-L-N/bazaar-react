import { useState } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { useCart } from '@/contexts/CartContext';
import { Trash2, Plus, Minus, ShoppingBag } from 'lucide-react';
import { toast } from 'sonner';

const Cart = () => {
  const { cart, removeFromCart, updateQuantity, cartTotal, clearCart } = useCart();
  const [isProcessing, setIsProcessing] = useState(false);

  const handleCheckout = async () => {
    setIsProcessing(true);
    // TODO: Implement actual checkout with API
    setTimeout(() => {
      toast.success('Order placed successfully!');
      clearCart();
      setIsProcessing(false);
    }, 1500);
  };

  if (cart.length === 0) {
    return (
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-1 container mx-auto px-4 py-16">
          <div className="text-center">
            <ShoppingBag className="h-24 w-24 mx-auto mb-4 text-muted-foreground/50" />
            <h2 className="text-3xl font-bold mb-4 text-foreground">Your cart is empty</h2>
            <p className="text-muted-foreground mb-8">
              Add some products to get started!
            </p>
            <Link to="/">
              <Button className="bg-accent hover:bg-accent/90 text-accent-foreground">
                Continue Shopping
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
        <h1 className="text-4xl font-bold mb-8 text-foreground">Shopping Cart</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2 space-y-4">
            {cart.map((item) => (
              <Card key={item.id} className="shadow-[var(--shadow-elegant)]">
                <CardContent className="p-4">
                  <div className="flex gap-4">
                    <img
                      src={item.image}
                      alt={item.title}
                      className="w-24 h-24 object-cover rounded-lg"
                    />
                    <div className="flex-1">
                      <h3 className="font-semibold mb-2 text-foreground">{item.title}</h3>
                      <p className="text-2xl font-bold text-foreground">
                        ${item.price.toFixed(2)}
                      </p>
                      <div className="flex items-center gap-2 mt-4">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        >
                          <Minus className="h-4 w-4" />
                        </Button>
                        <span className="w-12 text-center font-semibold text-foreground">
                          {item.quantity}
                        </span>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        >
                          <Plus className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => removeFromCart(item.id)}
                          className="ml-auto text-destructive hover:text-destructive"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <Card className="sticky top-24 shadow-[var(--shadow-elegant)]">
              <CardHeader>
                <CardTitle>Order Summary</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Subtotal</span>
                    <span className="font-semibold text-foreground">
                      ${cartTotal.toFixed(2)}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Shipping</span>
                    <span className="font-semibold text-accent">FREE</span>
                  </div>
                  <Separator />
                  <div className="flex justify-between text-lg font-bold">
                    <span className="text-foreground">Total</span>
                    <span className="text-accent">${cartTotal.toFixed(2)}</span>
                  </div>
                </div>

                <Button
                  onClick={handleCheckout}
                  disabled={isProcessing}
                  className="w-full bg-accent hover:bg-accent/90 text-accent-foreground"
                >
                  {isProcessing ? 'Processing...' : 'Proceed to Checkout'}
                </Button>

                <Link to="/" className="block">
                  <Button variant="outline" className="w-full">
                    Continue Shopping
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Cart;
