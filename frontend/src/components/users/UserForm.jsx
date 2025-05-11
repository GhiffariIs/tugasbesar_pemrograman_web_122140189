import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  FormControl,
  FormLabel,
  Input,
  Button,
  Select,
  VStack,
  useToast,
  Switch,
  FormHelperText
} from '@chakra-ui/react'
import { useState, useEffect } from 'react'

const UserForm = ({ isOpen, onClose, user }) => {
  const toast = useToast()
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    role: 'user',
    isActive: true
  })

  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name || '',
        email: user.email || '',
        password: '',
        role: user.role || 'user',
        isActive: user.isActive !== false
      })
    } else {
      setFormData({
        name: '',
        email: '',
        password: '',
        role: 'user',
        isActive: true
      })
    }
  }, [user])

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      // TODO: Implement API call
      const payload = { ...formData }
      if (!user) {
        // New user requires password
        if (!formData.password) {
          throw new Error('Password is required for new users')
        }
      } else if (!formData.password) {
        // Don't send empty password for existing users
        delete payload.password
      }

      // TODO: Call API service
      // await api.users.save(payload)

      toast({
        title: `User ${user ? 'updated' : 'created'} successfully.`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
      onClose()
    } catch (error) {
      toast({
        title: `Error ${user ? 'updating' : 'creating'} user.`,
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
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <form onSubmit={handleSubmit}>
          <ModalHeader>{user ? 'Edit User' : 'Add New User'}</ModalHeader>
          <ModalCloseButton />
          
          <ModalBody>
            <VStack spacing={4}>
              <FormControl isRequired>
                <FormLabel>Name</FormLabel>
                <Input
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="Enter full name"
                />
              </FormControl>

              <FormControl isRequired>
                <FormLabel>Email</FormLabel>
                <Input
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="Enter email address"
                />
              </FormControl>

              <FormControl isRequired={!user}>
                <FormLabel>{user ? 'New Password' : 'Password'}</FormLabel>
                <Input
                  name="password"
                  type="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder={user ? 'Leave blank to keep current' : 'Enter password'}
                />
                {user && (
                  <FormHelperText>
                    Leave blank to keep current password
                  </FormHelperText>
                )}
              </FormControl>

              <FormControl>
                <FormLabel>Role</FormLabel>
                <Select
                  name="role"
                  value={formData.role}
                  onChange={handleChange}
                >
                  <option value="user">User</option>
                  <option value="admin">Admin</option>
                </Select>
              </FormControl>

              <FormControl display="flex" alignItems="center">
                <FormLabel mb="0">Active</FormLabel>
                <Switch
                  name="isActive"
                  isChecked={formData.isActive}
                  onChange={handleChange}
                />
              </FormControl>
            </VStack>
          </ModalBody>

          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onClose}>
              Cancel
            </Button>
            <Button
              type="submit"
              colorScheme="brand"
              isLoading={isLoading}
            >
              {user ? 'Save Changes' : 'Create User'}
            </Button>
          </ModalFooter>
        </form>
      </ModalContent>
    </Modal>
  )
}

export default UserForm
