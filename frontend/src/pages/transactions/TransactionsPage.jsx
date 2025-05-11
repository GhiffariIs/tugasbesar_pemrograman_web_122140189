import { Box, Heading, Tab, TabList, TabPanel, TabPanels, Tabs } from '@chakra-ui/react'
import { useState } from 'react'

const TransactionsPage = () => {
  const [tabIndex, setTabIndex] = useState(0)

  return (
    <Box>
      <Heading size="lg" mb={6}>Transactions</Heading>
      
      <Tabs 
        colorScheme="brand" 
        onChange={(index) => setTabIndex(index)}
        value={tabIndex}
      >
        <TabList>
          <Tab>Recent Transactions</Tab>
          <Tab>Transaction History</Tab>
          <Tab>Stats</Tab>
        </TabList>

        <TabPanels>
          <TabPanel>
            {/* TODO: Add TransactionList component */}
            <Box>Recent transactions will be shown here</Box>
          </TabPanel>
          
          <TabPanel>
            {/* TODO: Add TransactionHistory component */}
            <Box>Transaction history will be shown here</Box>
          </TabPanel>
          
          <TabPanel>
            {/* TODO: Add TransactionStats component */}
            <Box>Transaction statistics will be shown here</Box>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  )
}

export default TransactionsPage
