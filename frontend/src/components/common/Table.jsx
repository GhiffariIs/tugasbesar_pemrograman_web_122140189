import {
  Table as ChakraTable,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Box,
  Text,
  Spinner,
  Center
} from '@chakra-ui/react'

const Table = ({
  columns,
  data,
  isLoading,
  emptyMessage = 'No data available',
}) => {
  if (isLoading) {
    return (
      <Center py={8}>
        <Spinner size="lg" />
      </Center>
    )
  }

  if (!data || data.length === 0) {
    return (
      <Center py={8}>
        <Text color="gray.500">{emptyMessage}</Text>
      </Center>
    )
  }

  return (
    <Box overflowX="auto">
      <ChakraTable variant="simple">
        <Thead>
          <Tr>
            {columns.map((column) => (
              <Th key={column.key}>
                {column.label}
              </Th>
            ))}
          </Tr>
        </Thead>
        <Tbody>
          {data.map((row, rowIndex) => (
            <Tr key={rowIndex}>
              {columns.map((column) => (
                <Td key={`${rowIndex}-${column.key}`}>
                  {column.render ? column.render(row) : row[column.key]}
                </Td>
              ))}
            </Tr>
          ))}
        </Tbody>
      </ChakraTable>
    </Box>
  )
}

export default Table