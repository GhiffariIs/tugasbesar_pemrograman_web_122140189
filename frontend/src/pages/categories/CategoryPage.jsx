import { Box, Heading, useDisclosure, Button } from '@chakra-ui/react'
import CategoryList from '../../components/categories/CategoryList'
import CategoryForm from '../../components/categories/CategoryForm'

const CategoryPage = () => {
  const { isOpen, onOpen, onClose } = useDisclosure()

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={6}>
        <Heading size="lg">Categories</Heading>
        <Button colorScheme="brand" onClick={onOpen}>
          Add Category
        </Button>
      </Box>

      <CategoryList />
      
      <CategoryForm isOpen={isOpen} onClose={onClose} />
    </Box>
  )
}

export default CategoryPage
