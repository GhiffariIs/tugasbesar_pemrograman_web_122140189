/**
 * Format date to Indonesian locale format
 * @param {string|Date} date - Date to format
 * @returns {string} Formatted date string
 */
export const formatDate = (date) => {
  if (!date) return '-';
  
  return new Date(date).toLocaleDateString('id-ID', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
};

/**
 * Format time to Indonesian locale format
 * @param {string|Date} date - Date to format
 * @returns {string} Formatted time string
 */
export const formatTime = (date) => {
  if (!date) return '-';
  
  return new Date(date).toLocaleTimeString('id-ID', {
    hour: '2-digit',
    minute: '2-digit',
  });
};

/**
 * Format date and time to Indonesian locale format
 * @param {string|Date} date - Date to format
 * @returns {string} Formatted date and time string
 */
export const formatDateTime = (date) => {
  if (!date) return '-';
  
  return new Date(date).toLocaleString('id-ID', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

/**
 * Format currency to Indonesian Rupiah format
 * @param {number} amount - Amount to format
 * @returns {string} Formatted currency string
 */
export const formatCurrency = (amount) => {
  if (amount === null || amount === undefined) return 'Rp 0';
  
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean} Whether the email is valid
 */
export const isValidEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

/**
 * Generate a random product code
 * @returns {string} Random product code
 */
export const generateProductCode = () => {
  const prefix = 'PRD';
  const randomDigits = Math.floor(1000 + Math.random() * 9000); // 4-digit number
  const timestamp = Date.now().toString().slice(-4); // Last 4 digits of timestamp
  
  return `${prefix}-${randomDigits}-${timestamp}`;
};

/**
 * Calculate percentage difference between two numbers
 * @param {number} current - Current value
 * @param {number} previous - Previous value
 * @returns {number} Percentage difference
 */
export const calculatePercentageDifference = (current, previous) => {
  if (!previous) return 0;
  return ((current - previous) / previous) * 100;
};
