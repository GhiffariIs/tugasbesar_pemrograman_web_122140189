// Jika ada component ProductDetail, pastikan juga menangani null/undefined

const ProductDetail = ({ product }) => {
  // Handle kasus product undefined/null
  if (!product) {
    return <Typography>No product data available</Typography>;
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6">{product.name || 'Unnamed Product'}</Typography>
        <Typography variant="body2">SKU: {product.sku || '-'}</Typography>
        <Typography variant="body2">
          Price: {product.price ? `Rp ${Number(product.price).toLocaleString('id-ID')}` : '-'}
        </Typography>
        <Typography variant="body2">
          Stock: {product.stock ?? 0}
        </Typography>
        <Typography variant="body2">
          Description: {product.description || 'No description'}
        </Typography>
      </CardContent>
    </Card>
  );
};