import { useState } from 'react'
import {
  Box,
  SimpleGrid,
  Input,
  InputGroup,
  InputLeftElement,
  Select,
  Stack,
  Text,
  Button,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  Badge,
  Flex
} from '@chakra-ui/react'
import { FiSearch, FiPlus, FiMinusCircle, FiPlusCircle } from 'react-icons/fi'
import ProductCard from './ProductCard'
import ProductForm from './ProductForm'

const StockUpdateModal = ({ isOpen, onClose, product, onUpdate }) => {
  const [quantity, setQuantity] = useState(0)
  const [type, setType] = useState('add')

  const handleSubmit = () => {
    onUpdate(product.id, quantity, type)
    onClose()
    setQuantity(0)
    setType('add')
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Update Stock - {product?.name}</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <Stack spacing={4}>
            <Flex justify="center" gap={4}>
              <Button
                leftIcon={<FiMinusCircle />}
                variant={type === 'remove' ? 'solid' : 'outline'}
                colorScheme="red"
                onClick={() => setType('remove')}
              >
                Remove
              </Button>
              <Button
                leftIcon={<FiPlusCircle />}
                variant={type === 'add' ? 'solid' : 'outline'}
                colorScheme="green"
                onClick={() => setType('add')}
              >
                Add
              </Button>
            </Flex>
            <NumberInput
              value={quantity}
              onChange={(_, value) => setQuantity(value)}
              min={0}
            >
              <NumberInputField placeholder="Enter quantity" />
              <NumberInputStepper>
                <NumberIncrementStepper />
                <NumberDecrementStepper />
              </NumberInputStepper>
            </NumberInput>
          </Stack>
        </ModalBody>
        <ModalFooter>
          <Button variant="ghost" mr={3} onClick={onClose}>
            Cancel
          </Button>
          <Button colorScheme={type === 'add' ? 'green' : 'red'} onClick={handleSubmit}>
            {type === 'add' ? 'Add Stock' : 'Remove Stock'}
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  )
}

const ProductList = ({ 
  products = [], 
  categories = [],
  onCreateProduct,
  onUpdateProduct,
  onDeleteProduct,
  onStockUpdate
}) => {
  const { 
    isOpen: isProductFormOpen, 
    onOpen: onProductFormOpen, 
    onClose: onProductFormClose 
  } = useDisclosure()
  const {
    isOpen: isStockUpdateOpen,
    onOpen: onStockUpdateOpen,
    onClose: onStockUpdateClose
  } = useDisclosure()
  const [searchQuery, setSearchQuery] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [stockUpdateProduct, setStockUpdateProduct] = useState(null)

  const handleEdit = (product) => {
    setSelectedProduct(product)
    onProductFormOpen()
  }

  const handleCreate = () => {
    setSelectedProduct(null)
    onProductFormOpen()
  }

  const handleFormSubmit = async (data) => {
    try {
      if (selectedProduct) {
        await onUpdateProduct(selectedProduct.id, data)
      } else {
        await onCreateProduct(data)
      }
      onProductFormClose()
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const handleStockUpdate = (product) => {
    setStockUpdateProduct(product)
    onStockUpdateOpen()
  }

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = !categoryFilter || product.category === categoryFilter
    return matchesSearch && matchesCategory
  })

  return (
    <Box>
      <Stack direction={{ base: 'column', md: 'row' }} spacing={4} mb={6}>
        <InputGroup maxW={{ base: 'full', md: '300px' }}>
          <InputLeftElement pointerEvents="none">
            <FiSearch color="gray.300" />
          </InputLeftElement>
          <Input
            placeholder="Search products..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </InputGroup>

        <Select
          placeholder="All Categories"
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          maxW={{ base: 'full', md: '200px' }}
        >
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </Select>

        <Button
          leftIcon={<FiPlus />}
          colorScheme="brand"
          onClick={handleCreate}
          ml="auto"
        >
          Add Product
        </Button>
      </Stack>

      {filteredProducts.length === 0 ? (
        <Text textAlign="center" py={8} color="gray.500">
          No products found
        </Text>
      ) : (
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
          {filteredProducts.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onEdit={() => handleEdit(product)}
              onDelete={() => onDeleteProduct(product.id)}
              onStockUpdate={() => handleStockUpdate(product)}
              showStockControls
            />
          ))}
        </SimpleGrid>
      )}

      <ProductForm
        isOpen={isProductFormOpen}
        onClose={onProductFormClose}
        onSubmit={handleFormSubmit}
        product={selectedProduct}
        categories={categories}
      />

      <StockUpdateModal
        isOpen={isStockUpdateOpen}
        onClose={onStockUpdateClose}
        product={stockUpdateProduct}
        onUpdate={onStockUpdate}
      />
    </Box>
  )
}

export default ProductList