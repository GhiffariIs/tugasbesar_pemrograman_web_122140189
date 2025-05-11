import { authApi } from './api'

export class AuthError extends Error {
  constructor(message) {
    super(message)
    this.name = 'AuthError'
  }
}

const authService = {
  /**
   * Login user with email and password
   * @param {string} email 
   * @param {string} password 
   * @returns {Promise<{token: string, user: object}>}
   */
  login: async (email, password) => {
    try {
      const response = await authApi.login({ email, password })
      if (response.token) {
        localStorage.setItem('token', response.token)
      }
      return response
    } catch (error) {
      throw new AuthError(error.message || 'Login failed')
    }
  },

  /**
   * Register new user
   * @param {object} userData 
   * @returns {Promise<{token: string, user: object}>}
   */
  register: async (userData) => {
    try {
      const response = await authApi.register(userData)
      if (response.token) {
        localStorage.setItem('token', response.token)
      }
      return response
    } catch (error) {
      throw new AuthError(error.message || 'Registration failed')
    }
  },

  /**
   * Get current user profile
   * @returns {Promise<object>}
   */
  getProfile: async () => {
    try {
      return await authApi.getProfile()
    } catch (error) {
      throw new AuthError(error.message || 'Failed to get profile')
    }
  },

  /**
   * Logout current user
   */
  logout: () => {
    localStorage.removeItem('token')
  },

  /**
   * Check if user is authenticated
   * @returns {boolean}
   */
  isAuthenticated: () => {
    return !!localStorage.getItem('token')
  },

  /**
   * Get authentication token
   * @returns {string|null}
   */
  getToken: () => {
    return localStorage.getItem('token')
  }
}

export default authService