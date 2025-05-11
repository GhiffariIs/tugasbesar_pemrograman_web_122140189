import {
  Box,
  Image,
  Badge,
  Text,
  Stack,
  Flex,
  IconButton,
  useColorModeValue,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Progress,
  Button,
  Tooltip
} from '@chakra-ui/react'
import { FiMoreVertical, FiEdit2, FiTrash2, FiPackage } from 'react-icons/fi'

const ProductCard = ({ 
  product, 
  onEdit, 
  onDelete,
  onStockUpdate,
  showStockControls = false
}) => {
  const bgColor = useColorModeValue('white', 'gray.700')
  const textColor = useColorModeValue('gray.600', 'gray.200')

  const getStockStatus = () => {
    if (product.stock === 0) {
      return { color: 'red', text: 'Out of Stock' }
    }
    if (product.stock <= product.minStock) {
      return { color: 'yellow', text: 'Low Stock' }
    }
    return { color: 'green', text: 'In Stock' }
  }

  const status = getStockStatus()
  const stockPercentage = Math.min((product.stock / (product.minStock * 3)) * 100, 100)

  return (
    <Box
      maxW="sm"
      borderWidth="1px"
      borderRadius="lg"
      overflow="hidden"
      bg={bgColor}
      position="relative"
    >
      <Image
        src={product.image || 'https://via.placeholder.com/300'}
        alt={product.name}
        height="200px"
        width="100%"
        objectFit="cover"
      />

      <Menu>
        <MenuButton
          as={IconButton}
          icon={<FiMoreVertical />}
          variant="ghost"
          size="sm"
          position="absolute"
          top="2"
          right="2"
        />
        <MenuList>
          <MenuItem icon={<FiEdit2 />} onClick={onEdit}>
            Edit
          </MenuItem>
          {showStockControls && (
            <MenuItem icon={<FiPackage />} onClick={onStockUpdate}>
              Update Stock
            </MenuItem>
          )}
          <MenuItem 
            icon={<FiTrash2 />} 
            onClick={() => onDelete(product.id)}
            color="red.500"
          >
            Delete
          </MenuItem>
        </MenuList>
      </Menu>

      <Stack p="4" spacing="3">
        <Flex justify="space-between" align="center">
          <Text
            fontSize="lg"
            fontWeight="semibold"
            lineHeight="short"
            isTruncated
          >
            {product.name}
          </Text>
          <Badge colorScheme={status.color}>{status.text}</Badge>
        </Flex>

        <Text fontSize="md" color={textColor}>
          {product.category}
        </Text>

        <Box>
          <Flex justify="space-between" mb={2}>
            <Text color={textColor}>Stock Level:</Text>
            <Text fontWeight="bold">{product.stock}</Text>
          </Flex>
          <Tooltip label={`Minimum stock: ${product.minStock}`}>
            <Progress 
              value={stockPercentage} 
              colorScheme={status.color}
              size="sm"
              borderRadius="full"
            />
          </Tooltip>
        </Box>

        <Flex justify="space-between" align="center">
          <Text fontSize="xl" fontWeight="bold" color="brand.500">
            ${product.price.toFixed(2)}
          </Text>
          {showStockControls && (
            <Button
              size="sm"
              leftIcon={<FiPackage />}
              onClick={onStockUpdate}
              colorScheme="brand"
              variant="outline"
            >
              Manage Stock
            </Button>
          )}
        </Flex>
      </Stack>
    </Box>
  )
}

export default ProductCard