import {
  Box,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Flex,
  Text,
  Badge,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td
} from '@chakra-ui/react'
import { FiPackage, FiAlertCircle, FiTrendingUp, FiTrendingDown } from 'react-icons/fi'
import StockChart from './StockChart'

const StatCard = ({ title, value, helpText, icon, trend }) => {
  return (
    <Stat
      px={4}
      py={3}
      bg="white"
      shadow="sm"
      rounded="lg"
      _dark={{ bg: 'gray.700' }}
    >
      <Flex justifyContent="space-between">
        <Box>
          <StatLabel color="gray.500">{title}</StatLabel>
          <StatNumber fontSize="2xl">{value}</StatNumber>
          <StatHelpText>
            {trend === 'up' && <FiTrendingUp style={{ display: 'inline' }} />}
            {trend === 'down' && <FiTrendingDown style={{ display: 'inline' }} />}
            {' '}{helpText}
          </StatHelpText>
        </Box>
        <Box
          p={2}
          rounded="md"
          bg="blue.50"
          color="blue.500"
          _dark={{ bg: 'blue.900' }}
        >
          {icon}
        </Box>
      </Flex>
    </Stat>
  )
}

const LowStockTable = ({ items }) => {
  return (
    <Box
      bg="white"
      shadow="sm"
      rounded="lg"
      p={4}
      _dark={{ bg: 'gray.700' }}
    >
      <Text fontSize="lg" fontWeight="medium" mb={4}>Low Stock Items</Text>
      <Table size="sm">
        <Thead>
          <Tr>
            <Th>Product</Th>
            <Th>Category</Th>
            <Th isNumeric>Stock</Th>
            <Th>Status</Th>
          </Tr>
        </Thead>
        <Tbody>
          {items.map((item) => (
            <Tr key={item.id}>
              <Td>{item.name}</Td>
              <Td>{item.category}</Td>
              <Td isNumeric>{item.stock}</Td>
              <Td>
                <Badge 
                  colorScheme={item.stock === 0 ? 'red' : 'yellow'}
                >
                  {item.stock === 0 ? 'Out of Stock' : 'Low Stock'}
                </Badge>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  )
}

const StockReport = ({ data = [] }) => {
  // Sample data if none is provided
  const sampleData = [
    { id: 1, name: 'Product A', category: 'Electronics', stock: 5, minStock: 10 },
    { id: 2, name: 'Product B', category: 'Clothing', stock: 0, minStock: 5 },
    { id: 3, name: 'Product C', category: 'Electronics', stock: 3, minStock: 8 },
    { id: 4, name: 'Product D', category: 'Food', stock: 2, minStock: 10 },
  ]

  const items = data.length > 0 ? data : sampleData
  const lowStockItems = items.filter(item => item.stock <= item.minStock)
  const totalItems = items.length
  const totalStock = items.reduce((sum, item) => sum + item.stock, 0)
  const outOfStock = items.filter(item => item.stock === 0).length

  return (
    <Box>
      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={5} mb={5}>
        <StatCard
          title="Total Products"
          value={totalItems}
          helpText="Total unique products"
          icon={<FiPackage size="20" />}
        />
        <StatCard
          title="Total Stock"
          value={totalStock}
          helpText="Items in inventory"
          icon={<FiPackage size="20" />}
        />
        <StatCard
          title="Low Stock Items"
          value={lowStockItems.length}
          helpText="Need attention"
          icon={<FiAlertCircle size="20" />}
          trend="up"
        />
        <StatCard
          title="Out of Stock"
          value={outOfStock}
          helpText="Items to reorder"
          icon={<FiAlertCircle size="20" />}
          trend={outOfStock > 0 ? 'up' : 'down'}
        />
      </SimpleGrid>

      <StockChart data={items} />
      
      {lowStockItems.length > 0 && (
        <Box mt={5}>
          <LowStockTable items={lowStockItems} />
        </Box>
      )}
    </Box>
  )
}

export default StockReport