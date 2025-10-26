import { useEffect, useState } from 'react';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ProductList from '@/components/ProductList';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { useAuth } from '@/contexts/AuthContext';
import { endpoints } from '@/lib/api';
import { Package } from 'lucide-react';

const Profile = () => {
  const { user } = useAuth();
  const [orders, setOrders] = useState<any[]>([]);
  const [viewHistory, setViewHistory] = useState<any[]>([]);

  useEffect(() => {
    if (!user) return;
    endpoints
      .getUserOrders(user.id)
      .then((res) => {
        const payload = res.data && res.data.data ? res.data.data : res.data;
        const raw = payload || [];
        // Normalize orders to the frontend shape used in the UI
        const normalized = (raw || []).map((o) => ({
          id: o.id || o._id || String(o.id),
          date: o.created_at || o.date || '',
          total: o.total_amount ?? o.total ?? 0,
          status: o.status || 'pending',
          items: (o.items || []).map((it) => ({
            id: it.product_id || it.product_id || '',
            title: it.product_name || it.title || '',
            quantity: it.quantity || 1,
            price: it.price ?? 0,
          })),
        }));
        setOrders(Array.isArray(normalized) ? normalized : []);
      })
      .catch((err) => console.error('Failed to load orders', err));

    endpoints
      .getUserHistory(user.id)
      .then((res) => {
        const payload = res.data && res.data.data ? res.data.data : res.data;
        const raw = payload || [];
        const transform = (p) => ({
          id: p.id || p._id || String(p.id),
          title: p.title || p.name || '',
          price: p.price ?? p.amount ?? 0,
          image: p.image || p.image_url || p.imageUrl || '',
          rating: p.rating ?? 0,
          reviews: p.review_count ?? p.reviews ?? 0,
          description: p.description || '',
          category: p.category || '',
          inStock: (p.stock_quantity ?? p.stock ?? 0) > 0,
        });
        setViewHistory(Array.isArray(raw) ? raw.map(transform) : []);
      })
      .catch((err) => console.error('Failed to load view history', err));
  }, [user]);

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      
      <main className="flex-1 container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-8 text-foreground">My Account</h1>

        {/* User Info */}
        <Card className="mb-8 shadow-[var(--shadow-elegant)]">
          <CardHeader>
            <CardTitle>Account Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Name:</span>
              <span className="font-semibold text-foreground">{user?.name}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Email:</span>
              <span className="font-semibold text-foreground">{user?.email}</span>
            </div>
          </CardContent>
        </Card>

        {/* Orders */}
        <Card className="mb-8 shadow-[var(--shadow-elegant)]">
          <CardHeader>
            <CardTitle>Order History</CardTitle>
            <CardDescription>View and track your orders</CardDescription>
          </CardHeader>
          <CardContent>
            {orders.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <Package className="h-12 w-12 mx-auto mb-2 opacity-50" />
                <p>No orders yet</p>
              </div>
            ) : (
              <div className="space-y-4">
                {orders.map((order) => (
                  <div key={order.id} className="border border-border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <p className="font-semibold text-foreground">Order #{order.id}</p>
                        <p className="text-sm text-muted-foreground">{order.date}</p>
                      </div>
                      <Badge
                        variant={order.status === 'Delivered' ? 'default' : 'secondary'}
                        className="bg-accent text-accent-foreground"
                      >
                        {order.status}
                      </Badge>
                    </div>
                    <Separator className="my-2" />
                    <div className="space-y-1">
                      {order.items.map((item) => (
                        <div key={item.id} className="flex justify-between text-sm">
                          <span className="text-foreground">
                            {item.title} x {item.quantity}
                          </span>
                          <span className="font-semibold text-foreground">
                            ${item.price.toFixed(2)}
                          </span>
                        </div>
                      ))}
                    </div>
                    <Separator className="my-2" />
                    <div className="flex justify-between font-bold">
                      <span className="text-foreground">Total:</span>
                      <span className="text-accent">${order.total.toFixed(2)}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Recently Viewed */}
        <div>
          <ProductList products={viewHistory} title="Recently Viewed" />
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Profile;
