import {
  FormControl,
  FormLabel,
  Input as ChakraInput,
  FormErrorMessage,
  FormHelperText,
  InputGroup,
  InputLeftElement,
  InputRightElement
} from '@chakra-ui/react'

const Input = ({
  label,
  error,
  helperText,
  leftElement,
  rightElement,
  isRequired,
  isInvalid,
  type = 'text',
  size = 'md',
  ...props
}) => {
  return (
    <FormControl 
      isRequired={isRequired} 
      isInvalid={isInvalid || !!error}
    >
      {label && <FormLabel>{label}</FormLabel>}
      
      <InputGroup size={size}>
        {leftElement && (
          <InputLeftElement pointerEvents="none">
            {leftElement}
          </InputLeftElement>
        )}

        <ChakraInput
          type={type}
          {...props}
          _hover={{
            borderColor: 'gray.300',
          }}
          _focus={{
            borderColor: 'blue.500',
            boxShadow: '0 0 0 1px var(--chakra-colors-blue-500)',
          }}
        />

        {rightElement && (
          <InputRightElement>
            {rightElement}
          </InputRightElement>
        )}
      </InputGroup>

      {error && (
        <FormErrorMessage>
          {error}
        </FormErrorMessage>
      )}

      {helperText && !error && (
        <FormHelperText>
          {helperText}
        </FormHelperText>
      )}
    </FormControl>
  )
}

export default Input