import { ChakraProvider, ColorModeScript } from '@chakra-ui/react'
import { 
  BrowserRouter, 
  createBrowserRouter, 
  RouterProvider 
} from 'react-router-dom'
import Routes from './routes'
import { AuthProvider } from './hooks/useAuth'
import theme from './theme'

const router = createBrowserRouter(Routes, {
  future: {
    v7_startTransition: true,
    v7_relativeSplatPath: true
  }
})

function App() {
  return (
    <ChakraProvider theme={theme}>
      <ColorModeScript initialColorMode={theme.config.initialColorMode} />
      <AuthProvider>
        <RouterProvider router={router} />
      </AuthProvider>
    </ChakraProvider>
  )
}

export default App
