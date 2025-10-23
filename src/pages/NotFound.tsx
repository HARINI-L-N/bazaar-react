import { useLocation, Link } from "react-router-dom";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Home, Search } from "lucide-react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="text-center px-4">
        <h1 className="mb-4 text-9xl font-bold text-primary">404</h1>
        <h2 className="mb-4 text-4xl font-bold text-foreground">Page Not Found</h2>
        <p className="mb-8 text-xl text-muted-foreground max-w-md mx-auto">
          Oops! The page you're looking for doesn't exist. It might have been moved or deleted.
        </p>
        <div className="flex gap-4 justify-center">
          <Link to="/">
            <Button className="bg-accent hover:bg-accent/90 text-accent-foreground">
              <Home className="h-4 w-4 mr-2" />
              Back to Home
            </Button>
          </Link>
          <Link to="/?search=">
            <Button variant="outline">
              <Search className="h-4 w-4 mr-2" />
              Search Products
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
