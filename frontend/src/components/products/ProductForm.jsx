import { useState } from 'react'
import {
  Box,
  VStack,
  FormControl,
  FormLabel,
  Input,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  Select,
  Textarea,
  Button,
  useToast
} from '@chakra-ui/react'

const ProductForm = ({ onSubmit, initialData = null, categories = [] }) => {
  const [formData, setFormData] = useState({
    name: initialData?.name || '',
    category: initialData?.category || '',
    price: initialData?.price || '',
    stock: initialData?.stock || '',
    minStock: initialData?.minStock || '',
    description: initialData?.description || '',
    image: initialData?.image || ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const toast = useToast()

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleNumberChange = (name, value) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      await onSubmit(formData)
      toast({
        title: `Product ${initialData ? 'updated' : 'created'} successfully`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      })

      if (!initialData) {
        // Clear form after successful creation
        setFormData({
          name: '',
          category: '',
          price: '',
          stock: '',
          minStock: '',
          description: '',
          image: ''
        })
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Box 
      as="form" 
      onSubmit={handleSubmit}
      p={6}
      bg="white"
      borderRadius="lg"
      boxShadow="sm"
      _dark={{
        bg: 'gray.700'
      }}
    >
      <VStack spacing={4}>
        <FormControl isRequired>
          <FormLabel>Product Name</FormLabel>
          <Input
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Enter product name"
          />
        </FormControl>

        <FormControl isRequired>
          <FormLabel>Category</FormLabel>
          <Select
            name="category"
            value={formData.category}
            onChange={handleChange}
            placeholder="Select category"
          >
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </Select>
        </FormControl>

        <FormControl isRequired>
          <FormLabel>Price</FormLabel>
          <NumberInput
            min={0}
            value={formData.price}
            onChange={(value) => handleNumberChange('price', value)}
          >
            <NumberInputField placeholder="Enter price" />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
        </FormControl>

        <FormControl isRequired>
          <FormLabel>Stock</FormLabel>
          <NumberInput
            min={0}
            value={formData.stock}
            onChange={(value) => handleNumberChange('stock', value)}
          >
            <NumberInputField placeholder="Enter current stock" />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
        </FormControl>

        <FormControl isRequired>
          <FormLabel>Minimum Stock</FormLabel>
          <NumberInput
            min={0}
            value={formData.minStock}
            onChange={(value) => handleNumberChange('minStock', value)}
          >
            <NumberInputField placeholder="Enter minimum stock level" />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
        </FormControl>

        <FormControl>
          <FormLabel>Description</FormLabel>
          <Textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Enter product description"
            resize="vertical"
          />
        </FormControl>

        <FormControl>
          <FormLabel>Image URL</FormLabel>
          <Input
            name="image"
            value={formData.image}
            onChange={handleChange}
            placeholder="Enter image URL"
          />
        </FormControl>

        <Button
          type="submit"
          colorScheme="blue"
          width="full"
          isLoading={isLoading}
        >
          {initialData ? 'Update Product' : 'Create Product'}
        </Button>
      </VStack>
    </Box>
  )
}

export default ProductForm