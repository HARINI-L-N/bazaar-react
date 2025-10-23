import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

const ProductCardSkeleton = () => {
  return (
    <Card className="h-full">
      <CardContent className="p-4">
        <Skeleton className="aspect-square mb-4 rounded-lg" />
        <Skeleton className="h-6 w-full mb-2" />
        <Skeleton className="h-6 w-3/4 mb-2" />
        <Skeleton className="h-4 w-1/2 mb-2" />
        <Skeleton className="h-8 w-1/3" />
      </CardContent>
      <CardFooter className="p-4 pt-0">
        <Skeleton className="h-10 w-full" />
      </CardFooter>
    </Card>
  );
};

export default ProductCardSkeleton;
