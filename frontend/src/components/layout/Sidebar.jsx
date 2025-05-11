import { Box, VStack, Icon, Link, Text, Drawer, DrawerOverlay, DrawerContent, DrawerCloseButton, DrawerHeader, DrawerBody, useColorModeValue } from '@chakra-ui/react'
import { NavLink as RouterLink } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { 
  FiHome, 
  FiBox, 
  FiList, 
  FiShoppingBag, 
  FiBarChart2,
  FiUsers,
  FiSettings 
} from 'react-icons/fi'

const NavItem = ({ icon, children, to }) => {
  return (
    <Link
      as={RouterLink}
      to={to}
      style={{ textDecoration: 'none' }}
      _focus={{ boxShadow: 'none' }}
    >
      {({ isActive }) => (
        <Box
          display="flex"
          alignItems="center"
          py={3}
          px={4}
          borderRadius="lg"
          role="group"
          cursor="pointer"
          _hover={{
            bg: 'gray.100',
            color: 'black',
          }}
          bg={isActive ? 'gray.100' : 'transparent'}
          color={isActive ? 'black' : 'gray.600'}
          _dark={{
            _hover: { bg: 'gray.700', color: 'white' },
            bg: isActive ? 'gray.700' : 'transparent',
            color: isActive ? 'white' : 'gray.400',
          }}
        >
          <Icon
            mr={4}
            fontSize="16"
            as={icon}
          />
          <Text fontSize="sm" fontWeight="medium">
            {children}
          </Text>
        </Box>
      )}
    </Link>
  )
}

const Sidebar = ({ isOpen, onClose, isMobile }) => {
  const { user } = useAuth()
  const bgColor = useColorModeValue('white', 'gray.900')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  const navigation = [
    { name: 'Dashboard', icon: FiHome, to: '/', role: 'user' },
    { name: 'Products', icon: FiBox, to: '/products', role: 'user' },
    { name: 'Categories', icon: FiList, to: '/categories', role: 'user' },
    { name: 'Transactions', icon: FiShoppingBag, to: '/transactions', role: 'user' },
    { name: 'Reports', icon: FiBarChart2, to: '/reports', role: 'admin' },
    { name: 'Users', icon: FiUsers, to: '/users', role: 'admin' },
    { name: 'Settings', icon: FiSettings, to: '/settings', role: 'admin' }
  ]

  const SidebarContent = () => (
    <VStack py={5} spacing={1} align="stretch">
      {navigation.map((item) => (
        ((user?.role === 'admin') || (item.role === 'user')) && (
          <NavItem key={item.name} icon={item.icon} to={item.to}>
            {item.name}
          </NavItem>
        )
      ))}
    </VStack>
  )

  if (isMobile) {
    return (
      <Drawer
        autoFocus={false}
        isOpen={isOpen}
        placement="left"
        onClose={onClose}
        returnFocusOnClose={false}
        onOverlayClick={onClose}
        size="full"
      >
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader borderBottomWidth="1px">Aturmation Menu</DrawerHeader>
          <DrawerBody>
            <SidebarContent />
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    )
  }

  return (
    <Box
      as="nav"
      pos="fixed"
      top="0"
      left="0"
      w="60"
      h="100vh"
      bg={bgColor}
      borderRight="1px"
      borderColor={borderColor}
      zIndex="sticky"
      display={{ base: 'none', md: 'block' }}
      transition="3s ease"
    >
      <SidebarContent />
    </Box>
  )
}

export default Sidebar