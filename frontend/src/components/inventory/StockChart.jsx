import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'
import { Box, Text, Select, Flex } from '@chakra-ui/react'
import { useState } from 'react'

const StockChart = ({ data = [] }) => {
  const [chartType, setChartType] = useState('category') // 'category' or 'product'

  const processData = () => {
    if (chartType === 'category') {
      // Group by category and sum stock levels
      return data.reduce((acc, item) => {
        const existingCategory = acc.find(c => c.name === item.category)
        if (existingCategory) {
          existingCategory.stock += item.stock
        } else {
          acc.push({ name: item.category, stock: item.stock })
        }
        return acc
      }, [])
    }
    
    // Return top 10 products by stock level
    return [...data]
      .sort((a, b) => b.stock - a.stock)
      .slice(0, 10)
      .map(item => ({
        name: item.name,
        stock: item.stock
      }))
  }

  return (
    <Box p={4} bg="white" borderRadius="lg" shadow="sm" _dark={{ bg: 'gray.700' }}>
      <Flex justify="space-between" align="center" mb={4}>
        <Text fontSize="lg" fontWeight="medium">Stock Levels</Text>
        <Select 
          value={chartType}
          onChange={(e) => setChartType(e.target.value)}
          width="200px"
        >
          <option value="category">By Category</option>
          <option value="product">Top 10 Products</option>
        </Select>
      </Flex>

      <Box height="400px">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={processData()}
            margin={{
              top: 20,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="name" 
              angle={-45}
              textAnchor="end"
              height={70}
            />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar 
              dataKey="stock" 
              fill="#3182CE"
              name="Stock Level"
            />
          </BarChart>
        </ResponsiveContainer>
      </Box>
    </Box>
  )
}

export default StockChart