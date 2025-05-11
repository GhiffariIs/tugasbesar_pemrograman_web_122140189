import { useState, useEffect, useCallback } from 'react'
import {
  Box,
  Heading,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  SimpleGrid,
  useToast,
  Spinner,
  Center,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Select
} from '@chakra-ui/react'
import StockChart from '../../components/inventory/StockChart'
import StockReport from '../../components/inventory/StockReport'
import ProductList from '../../components/products/ProductList'
import { stockApi } from '../../services/api'

const InventoryPage = () => {
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)
  const [timeRange, setTimeRange] = useState('week')
  const [stockData, setStockData] = useState(null)
  const toast = useToast()

  const fetchStockData = useCallback(async () => {
    try {
      setIsLoading(true)
      setError(null)
      const data = await stockApi.getStockReport(timeRange)
      setStockData(data)
    } catch (err) {
      setError(err.message || 'Error fetching inventory data')
      toast({
        title: 'Error fetching inventory data',
        description: err.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    } finally {
      setIsLoading(false)
    }
  }, [timeRange, toast])

  useEffect(() => {
    fetchStockData()
  }, [fetchStockData])

  const handleStockUpdate = async (productId, quantity, type = 'set') => {
    try {
      await stockApi.updateStock(productId, quantity, type)
      await fetchStockData() // Refresh data
      toast({
        title: 'Stock updated successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
    } catch (error) {
      toast({
        title: 'Error updating stock',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
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
    <Box p={4}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={6}>
        <Heading>Inventory Management</Heading>
        <Select
          width="200px"
          value={timeRange}
          onChange={(e) => setTimeRange(e.target.value)}
        >
          <option value="week">Last 7 Days</option>
          <option value="month">Last 30 Days</option>
          <option value="quarter">Last 3 Months</option>
          <option value="year">Last Year</option>
        </Select>
      </Box>

      <Tabs colorScheme="brand" isLazy>
        <TabList>
          <Tab>Overview</Tab>
          <Tab>Stock Management</Tab>
          <Tab>Reports</Tab>
        </TabList>

        <TabPanels>
          {/* Overview Tab */}
          <TabPanel>
            <SimpleGrid columns={{ base: 1, lg: 2 }} spacing={6}>
              <StockChart data={stockData?.stockLevels} timeRange={timeRange} />
              <StockReport data={stockData?.products} />
            </SimpleGrid>
          </TabPanel>

          {/* Stock Management Tab */}
          <TabPanel>
            <ProductList
              products={stockData?.products}
              onStockUpdate={handleStockUpdate}
              categories={stockData?.categories}
              isLoading={isLoading}
            />
          </TabPanel>

          {/* Reports Tab */}
          <TabPanel>
            <StockReport 
              data={stockData?.products}
              showDetails
            />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  )
}

export default InventoryPage