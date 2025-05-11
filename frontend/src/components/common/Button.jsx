import { Button as ChakraButton } from '@chakra-ui/react'

const Button = ({ 
  children, 
  variant = 'solid', 
  colorScheme = 'blue',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  ...props 
}) => {
  return (
    <ChakraButton
      variant={variant}
      colorScheme={colorScheme}
      size={size}
      isLoading={isLoading}
      leftIcon={leftIcon}
      rightIcon={rightIcon}
      _hover={{
        transform: 'translateY(-1px)',
        boxShadow: 'md',
      }}
      _active={{
        transform: 'translateY(0)',
        boxShadow: 'sm',
      }}
      {...props}
    >
      {children}
    </ChakraButton>
  )
}

export default Button