import { Box, Heading, Grid, GridItem, Card, CardHeader, CardBody, Text, Select } from '@chakra-ui/react'
import StockChart from '../../components/inventory/StockChart'
import StockReport from '../../components/inventory/StockReport'
import { useState } from 'react'

const ReportsPage = () => {
  const [timeRange, setTimeRange] = useState('week')

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={6}>
        <Heading size="lg">Reports & Analytics</Heading>
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

      <Grid templateColumns="repeat(12, 1fr)" gap={6}>
        {/* Stock Level Overview */}
        <GridItem colSpan={{ base: 12, lg: 8 }}>
          <Card>
            <CardHeader>
              <Heading size="md">Stock Levels Overview</Heading>
            </CardHeader>
            <CardBody>
              <StockChart timeRange={timeRange} />
            </CardBody>
          </Card>
        </GridItem>

        {/* Quick Stats */}
        <GridItem colSpan={{ base: 12, lg: 4 }}>
          <Card>
            <CardHeader>
              <Heading size="md">Quick Stats</Heading>
            </CardHeader>
            <CardBody>
              <StockReport />
            </CardBody>
          </Card>
        </GridItem>

        {/* Low Stock Alerts */}
        <GridItem colSpan={{ base: 12, md: 6 }}>
          <Card>
            <CardHeader>
              <Heading size="md">Low Stock Alerts</Heading>
            </CardHeader>
            <CardBody>
              {/* TODO: Add LowStockAlerts component */}
              <Text>Low stock alerts will be shown here</Text>
            </CardBody>
          </Card>
        </GridItem>

        {/* Top Moving Products */}
        <GridItem colSpan={{ base: 12, md: 6 }}>
          <Card>
            <CardHeader>
              <Heading size="md">Top Moving Products</Heading>
            </CardHeader>
            <CardBody>
              {/* TODO: Add TopMovingProducts component */}
              <Text>Top moving products will be shown here</Text>
            </CardBody>
          </Card>
        </GridItem>
      </Grid>
    </Box>
  )
}

export default ReportsPage
