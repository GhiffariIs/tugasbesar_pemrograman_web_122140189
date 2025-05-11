import { 
  Box, 
  Heading, 
  Table, 
  Thead, 
  Tbody, 
  Tr, 
  Th, 
  Td, 
  Button,
  IconButton,
  useDisclosure,
  useToast,
  Badge,
  Spinner,
  Center,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription
} from '@chakra-ui/react'
import { FiEdit2, FiTrash2 } from 'react-icons/fi'
import { useState, useEffect, useCallback } from 'react'
import { usersApi } from '../../services/api'
import UserForm from '../../components/users/UserForm'

const UsersPage = () => {
  const toast = useToast()
  const { isOpen, onOpen, onClose } = useDisclosure()
  const [selectedUser, setSelectedUser] = useState(null)
  const [users, setUsers] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchUsers = useCallback(async () => {
    try {
      setIsLoading(true)
      setError(null)
      const data = await usersApi.getAll()
      setUsers(data)
    } catch (err) {
      setError(err.message || 'Error fetching users')
      toast({
        title: 'Error fetching users',
        description: err.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    } finally {
      setIsLoading(false)
    }
  }, [toast])
  useEffect(() => {
    fetchUsers()
  }, [fetchUsers])

  const handleEdit = (user) => {
    setSelectedUser(user)
    onOpen()
  }

  const handleDelete = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) {
      return
    }

    try {
      await usersApi.delete(userId)
      setUsers(users.filter(user => user.id !== userId))
      
      toast({
        title: 'User deleted successfully.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
    } catch (error) {
      toast({
        title: 'Error deleting user.',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  }

  const handleFormClose = () => {
    setSelectedUser(null)
    onClose()
    fetchUsers() // Refresh the list after form closes
  }

  if (isLoading) {
    return (
      <Center h="200px">
        <Spinner size="xl" color="brand.500" />
      </Center>
    )
  }

  if (error) {
    return (
      <Alert status="error">
        <AlertIcon />
        <AlertTitle>Error!</AlertTitle>
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    )
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={6}>
        <Heading size="lg">Users Management</Heading>
        <Button colorScheme="brand" onClick={() => { setSelectedUser(null); onOpen(); }}>
          Add User
        </Button>
      </Box>

      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Name</Th>
            <Th>Email</Th>
            <Th>Role</Th>
            <Th>Status</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {users.map(user => (
            <Tr key={user.id}>
              <Td>{user.name}</Td>
              <Td>{user.email}</Td>
              <Td>
                <Badge colorScheme={user.role === 'admin' ? 'purple' : 'blue'}>
                  {user.role}
                </Badge>
              </Td>
              <Td>
                <Badge colorScheme={user.isActive ? 'green' : 'red'}>
                  {user.isActive ? 'Active' : 'Inactive'}
                </Badge>
              </Td>
              <Td>
                <IconButton
                  icon={<FiEdit2 />}
                  aria-label="Edit user"
                  mr={2}
                  onClick={() => handleEdit(user)}
                />
                <IconButton
                  icon={<FiTrash2 />}
                  aria-label="Delete user"
                  colorScheme="red"
                  onClick={() => handleDelete(user.id)}
                />
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>

      <UserForm 
        isOpen={isOpen} 
        onClose={handleFormClose} 
        user={selectedUser}
      />
    </Box>
  )
}

export default UsersPage
