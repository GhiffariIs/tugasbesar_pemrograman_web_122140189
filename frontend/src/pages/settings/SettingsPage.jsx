import {
  Box,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Switch,
  Button,
  VStack,
  Divider,
  useToast,
  Card,
  CardHeader,
  CardBody
} from '@chakra-ui/react'
import { useState } from 'react'

const SettingsPage = () => {
  const toast = useToast()
  const [settings, setSettings] = useState({
    companyName: 'Aturmation',
    lowStockThreshold: 10,
    enableNotifications: true,
    emailNotifications: true,
    autoReorder: false,
    reorderThreshold: 5
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      // TODO: Implement settings update
      toast({
        title: 'Settings updated.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
    } catch (error) {
      toast({
        title: 'Error updating settings.',
        description: error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  }

  return (
    <Box>
      <Heading size="lg" mb={6}>System Settings</Heading>

      <form onSubmit={handleSubmit}>
        <VStack spacing={6} align="stretch">
          {/* General Settings */}
          <Card>
            <CardHeader>
              <Heading size="md">General Settings</Heading>
            </CardHeader>
            <CardBody>
              <VStack spacing={4} align="stretch">
                <FormControl>
                  <FormLabel>Company Name</FormLabel>
                  <Input
                    name="companyName"
                    value={settings.companyName}
                    onChange={handleChange}
                  />
                </FormControl>

                <FormControl>
                  <FormLabel>Low Stock Threshold</FormLabel>
                  <Input
                    name="lowStockThreshold"
                    type="number"
                    value={settings.lowStockThreshold}
                    onChange={handleChange}
                  />
                </FormControl>
              </VStack>
            </CardBody>
          </Card>

          {/* Notification Settings */}
          <Card>
            <CardHeader>
              <Heading size="md">Notification Settings</Heading>
            </CardHeader>
            <CardBody>
              <VStack spacing={4} align="stretch">
                <FormControl display="flex" alignItems="center">
                  <FormLabel mb="0">Enable Notifications</FormLabel>
                  <Switch
                    name="enableNotifications"
                    isChecked={settings.enableNotifications}
                    onChange={handleChange}
                  />
                </FormControl>

                <FormControl display="flex" alignItems="center">
                  <FormLabel mb="0">Email Notifications</FormLabel>
                  <Switch
                    name="emailNotifications"
                    isChecked={settings.emailNotifications}
                    onChange={handleChange}
                  />
                </FormControl>
              </VStack>
            </CardBody>
          </Card>

          {/* Automation Settings */}
          <Card>
            <CardHeader>
              <Heading size="md">Automation Settings</Heading>
            </CardHeader>
            <CardBody>
              <VStack spacing={4} align="stretch">
                <FormControl display="flex" alignItems="center">
                  <FormLabel mb="0">Auto Reorder</FormLabel>
                  <Switch
                    name="autoReorder"
                    isChecked={settings.autoReorder}
                    onChange={handleChange}
                  />
                </FormControl>

                <FormControl>
                  <FormLabel>Reorder Threshold</FormLabel>
                  <Input
                    name="reorderThreshold"
                    type="number"
                    value={settings.reorderThreshold}
                    onChange={handleChange}
                  />
                </FormControl>
              </VStack>
            </CardBody>
          </Card>

          <Button type="submit" colorScheme="brand" size="lg">
            Save Settings
          </Button>
        </VStack>
      </form>
    </Box>
  )
}

export default SettingsPage
