import { useState } from 'react'
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  IconButton,
  useToast,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Text,
  Stack,
  Button,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton
} from '@chakra-ui/react'
import { FiMoreVertical, FiEdit2, FiTrash2, FiPlus } from 'react-icons/fi'
import CategoryForm from './CategoryForm'

const CategoryList = ({ categories = [], onUpdate, onDelete, onCreate }) => {
  const [selectedCategory, setSelectedCategory] = useState(null)
  const { isOpen, onOpen, onClose } = useDisclosure()
  const toast = useToast()

  const handleEdit = (category) => {
    setSelectedCategory(category)
    onOpen()
  }

  const handleDelete = async (categoryId) => {
    try {
      await onDelete(categoryId)
      toast({
        title: 'Category deleted successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
    } catch (error) {
      toast({
        title: 'Error deleting category',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  }

  const handleCreate = () => {
    setSelectedCategory(null)
    onOpen()
  }

  const handleFormSubmit = async (data) => {
    if (selectedCategory) {
      await onUpdate(selectedCategory.id, data)
    } else {
      await onCreate(data)
    }
    onClose()
  }

  return (
    <Box>
      <Stack direction="row" justifyContent="space-between" mb={4}>
        <Text fontSize="xl" fontWeight="bold">Categories</Text>
        <Button
          leftIcon={<FiPlus />}
          colorScheme="blue"
          onClick={handleCreate}
        >
          Add Category
        </Button>
      </Stack>

      <Box overflowX="auto">
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>Name</Th>
              <Th>Description</Th>
              <Th width="50px">Actions</Th>
            </Tr>
          </Thead>
          <Tbody>
            {categories.map((category) => (
              <Tr key={category.id}>
                <Td>{category.name}</Td>
                <Td>{category.description}</Td>
                <Td>
                  <Menu>
                    <MenuButton
                      as={IconButton}
                      icon={<FiMoreVertical />}
                      variant="ghost"
                      size="sm"
                    />
                    <MenuList>
                      <MenuItem 
                        icon={<FiEdit2 />} 
                        onClick={() => handleEdit(category)}
                      >
                        Edit
                      </MenuItem>
                      <MenuItem 
                        icon={<FiTrash2 />} 
                        onClick={() => handleDelete(category.id)}
                        color="red.500"
                      >
                        Delete
                      </MenuItem>
                    </MenuList>
                  </Menu>
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>
            {selectedCategory ? 'Edit Category' : 'Add Category'}
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <CategoryForm
              onSubmit={handleFormSubmit}
              initialData={selectedCategory}
            />
          </ModalBody>
        </ModalContent>
      </Modal>
    </Box>
  )
}

export default CategoryList