import ProductCard from './ProductCard';

interface Product {
  id: string;
  title: string;
  price: number;
  image: string;
  rating: number;
  reviews: number;
}

interface ProductListProps {
  products: Product[];
  title?: string;
}

const ProductList = ({ products, title }: ProductListProps) => {
  return (
    <div className="py-8">
      {title && (
        <h2 className="text-3xl font-bold mb-6 text-foreground">{title}</h2>
      )}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {products.map((product) => (
          <ProductCard key={product.id} {...product} />
        ))}
      </div>
    </div>
  );
};

export default ProductList;
