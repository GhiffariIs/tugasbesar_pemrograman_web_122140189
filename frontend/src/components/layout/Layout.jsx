import { Box, Flex, useDisclosure, useBreakpointValue } from '@chakra-ui/react'
import { Outlet } from 'react-router-dom'
import Navbar from './Navbar'
import Sidebar from './Sidebar'

const Layout = () => {
  const { isOpen, onOpen, onClose } = useDisclosure()
  const isMobile = useBreakpointValue({ base: true, md: false })

  return (
    <Box minH="100vh">
      <Sidebar 
        onClose={onClose} 
        isOpen={isOpen} 
        isMobile={isMobile}
      />
      <Box 
        ml={{ base: 0, md: 60 }} 
        transition=".3s ease"
      >
        <Navbar onOpen={onOpen} />
        <Box
          as="main"
          p="4"
          minH="calc(100vh - 64px)"
          mt="16"
          bg="gray.50"
          _dark={{
            bg: "gray.800"
          }}
        >
          <Outlet />
        </Box>
      </Box>
    </Box>
  )
}

export default Layout