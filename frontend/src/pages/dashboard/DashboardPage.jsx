import { Box, SimpleGrid, Heading } from '@chakra-ui/react'
import { FiBox, FiAlertCircle, FiShoppingBag } from 'react-icons/fi'
import StockChart from '../../components/inventory/StockChart'
import StockReport from '../../components/inventory/StockReport'

const DashboardPage = () => {
  // Sample data - replace with actual API calls
  const stockData = {
    totalProducts: 150,
    totalStock: 2500,
    outOfStock: 5,
    lowStock: 12,
    recentTransactions: [
      {
        id: 1,
        type: 'in',
        quantity: 100,
        productName: 'Product A',
        date: '2024-05-10'
      },
      // ... more transactions
    ],
    products: [
      {
        id: 1,
        name: 'Product A',
        category: 'Electronics',
        stock: 50,
        minStock: 10
      },
      // ... more products
    ]
  }

  return (
    <Box p={4}>
      <Heading mb={6}>Dashboard</Heading>

      {/* Statistics Overview */}
      <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6} mb={8}>
        <Box 
          p={6} 
          bg="white" 
          rounded="lg" 
          shadow="sm"
          _dark={{ bg: 'gray.700' }}
        >
          <StockReport 
            data={stockData.products}
            title="Inventory Overview"
          />
        </Box>
      </SimpleGrid>

      {/* Charts and Reports */}
      <SimpleGrid columns={{ base: 1, lg: 2 }} spacing={6}>
        {/* Stock Level Chart */}
        <Box 
          p={6} 
          bg="white" 
          rounded="lg" 
          shadow="sm"
          _dark={{ bg: 'gray.700' }}
        >
          <StockChart 
            data={stockData.products}
            title="Stock Levels by Category"
          />
        </Box>

        {/* Recent Activity / Low Stock Items */}
        <Box 
          p={6} 
          bg="white" 
          rounded="lg" 
          shadow="sm"
          _dark={{ bg: 'gray.700' }}
        >
          <StockReport 
            data={stockData.products.filter(p => p.stock <= p.minStock)}
            title="Low Stock Items"
            showChart={false}
          />
        </Box>
      </SimpleGrid>
    </Box>
  )
}

export default DashboardPage