/**
 * Format price to currency string
 * @param {number} price 
 * @param {string} currency 
 * @returns {string}
 */
export const formatPrice = (price, currency = 'USD') => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency
  }).format(price)
}

/**
 * Format date to readable string
 * @param {string|Date} date 
 * @returns {string}
 */
export const formatDate = (date) => {
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(new Date(date))
}

/**
 * Validate email format
 * @param {string} email 
 * @returns {boolean}
 */
export const isValidEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(email)
}

/**
 * Truncate text to specified length
 * @param {string} text 
 * @param {number} length 
 * @returns {string}
 */
export const truncateText = (text, length = 50) => {
  if (!text) return ''
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}

/**
 * Get stock status color
 * @param {number} stock 
 * @param {number} minStock 
 * @returns {string}
 */
export const getStockStatusColor = (stock, minStock) => {
  if (stock === 0) return 'red'
  if (stock <= minStock) return 'yellow'
  return 'green'
}

/**
 * Get stock status text
 * @param {number} stock 
 * @param {number} minStock 
 * @returns {string}
 */
export const getStockStatusText = (stock, minStock) => {
  if (stock === 0) return 'Out of Stock'
  if (stock <= minStock) return 'Low Stock'
  return 'In Stock'
}

/**
 * Sort array by key
 * @param {Array} array 
 * @param {string} key 
 * @param {string} order 
 * @returns {Array}
 */
export const sortArrayByKey = (array, key, order = 'asc') => {
  return [...array].sort((a, b) => {
    if (order === 'asc') {
      return a[key] > b[key] ? 1 : -1
    }
    return a[key] < b[key] ? 1 : -1
  })
}

/**
 * Filter array by search text
 * @param {Array} array 
 * @param {string} searchText 
 * @param {Array} keys 
 * @returns {Array}
 */
export const filterArrayBySearch = (array, searchText, keys) => {
  if (!searchText) return array
  
  const lowercasedSearch = searchText.toLowerCase()
  return array.filter(item => {
    return keys.some(key => {
      const value = item[key]
      return value && value.toString().toLowerCase().includes(lowercasedSearch)
    })
  })
}

/**
 * Generate random ID
 * @returns {string}
 */
export const generateId = () => {
  return Math.random().toString(36).substring(2) + Date.now().toString(36)
}