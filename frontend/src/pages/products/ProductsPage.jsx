import { useState } from 'react'
import {
  Box,
  Heading,
  SimpleGrid,
  useDisclosure,
  useToast,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
} from '@chakra-ui/react'
import ProductList from '../../components/products/ProductList'
import ProductForm from '../../components/products/ProductForm'

const ProductsPage = () => {
  const [products, setProducts] = useState([
    {
      id: 1,
      name: 'Product A',
      category: 'Electronics',
      price: 299.99,
      stock: 50,
      minStock: 10,
      description: 'Product A description',
      image: 'https://via.placeholder.com/150'
    }
    // ... more products
  ])

  const [categories] = useState([
    { id: 1, name: 'Electronics' },
    { id: 2, name: 'Books' },
    { id: 3, name: 'Clothing' }
  ])

  const { isOpen, onOpen, onClose } = useDisclosure()
  const [selectedProduct, setSelectedProduct] = useState(null)
  const toast = useToast()

  const handleCreateProduct = async (data) => {
    try {
      // Replace with actual API call
      const newProduct = {
        id: Date.now(),
        ...data
      }
      setProducts([...products, newProduct])
      onClose()
      toast({
        title: 'Product created successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
    } catch (error) {
      toast({
        title: 'Error creating product',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  }

  const handleUpdateProduct = async (id, data) => {
    try {
      // Replace with actual API call
      const updatedProducts = products.map(product =>
        product.id === id ? { ...product, ...data } : product
      )
      setProducts(updatedProducts)
      onClose()
      toast({
        title: 'Product updated successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
    } catch (error) {
      toast({
        title: 'Error updating product',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  }

  const handleDeleteProduct = async (id) => {
    try {
      // Replace with actual API call
      setProducts(products.filter(product => product.id !== id))
      toast({
        title: 'Product deleted successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
    } catch (error) {
      toast({
        title: 'Error deleting product',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  }

  const handleEdit = (product) => {
    setSelectedProduct(product)
    onOpen()
  }

  const handleCreate = () => {
    setSelectedProduct(null)
    onOpen()
  }

  return (
    <Box p={4}>
      <Heading mb={6}>Products</Heading>

      <ProductList
        products={products}
        categories={categories}
        onCreateProduct={handleCreate}
        onUpdateProduct={handleEdit}
        onDeleteProduct={handleDeleteProduct}
      />

      <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>
            {selectedProduct ? 'Edit Product' : 'Create Product'}
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <ProductForm
              initialData={selectedProduct}
              categories={categories}
              onSubmit={selectedProduct 
                ? (data) => handleUpdateProduct(selectedProduct.id, data)
                : handleCreateProduct
              }
            />
          </ModalBody>
        </ModalContent>
      </Modal>
    </Box>
  )
}

export default ProductsPage