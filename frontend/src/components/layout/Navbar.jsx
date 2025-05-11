import { Box, Flex, IconButton, useColorMode, useColorModeValue, Button, Text } from '@chakra-ui/react'
import { FiMenu, FiSun, FiMoon, FiBell, FiUser } from 'react-icons/fi'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'

const Navbar = ({ onOpen }) => {
  const { colorMode, toggleColorMode } = useColorMode()
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  
  const bgColor = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  return (
    <Box
      px={4}
      bg={bgColor}
      borderBottom="1px"
      borderColor={borderColor}
      position="fixed"
      w="100%"
      zIndex="sticky"
    >
      <Flex h={16} alignItems="center" justifyContent="space-between">
        <IconButton
          variant="ghost"
          onClick={onOpen}
          aria-label="open menu"
          icon={<FiMenu />}
        />

        <Text
          fontSize="xl"
          fontWeight="bold"
          color="brand.500"
          cursor="pointer"
          onClick={() => navigate('/')}
        >
          Aturmation
        </Text>

        <Flex alignItems="center" gap={4}>
          <IconButton
            aria-label="Toggle color mode"
            icon={colorMode === 'light' ? <FiMoon /> : <FiSun />}
            onClick={toggleColorMode}
          />
          
          {user && (
            <>
              <IconButton
                aria-label="Notifications"
                icon={<FiBell />}
                variant="ghost"
              />
              <IconButton
                aria-label="User menu"
                icon={<FiUser />}
                variant="ghost"
              />
              <Button variant="ghost" onClick={logout}>
                Logout
              </Button>
            </>
          )}
          
          {!user && (
            <Button onClick={() => navigate('/login')}>
              Login
            </Button>
          )}
        </Flex>
      </Flex>
    </Box>
  )
}

export default Navbar