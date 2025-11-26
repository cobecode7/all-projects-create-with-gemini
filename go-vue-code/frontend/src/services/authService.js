import http from './httpService';

const TOKEN_KEY = 'auth_token';

export default {
  // Login
  async login(credentials) {
    const response = await http.post('/auth/login', credentials);
    this.setToken(response.data.token);
    return response.data;
  },

  // Logout
  async logout() {
    try {
      await http.post('/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      this.removeToken();
    }
  },

  // Register
  async register(userData) {
    const response = await http.post('/auth/register', userData);
    return response.data;
  },

  // Request password reset
  async requestPasswordReset(email) {
    const response = await http.post('/auth/password/email', { email });
    return response.data;
  },

  // Reset password
  async resetPassword(token, password, passwordConfirmation) {
    const response = await http.post('/auth/password/reset', {
      token,
      password,
      password_confirmation: passwordConfirmation
    });
    return response.data;
  },

  // Send email verification
  async sendEmailVerification() {
    const response = await http.post('/auth/email/verification-notification');
    return response.data;
  },

  // Verify email
  async verifyEmail(id, hash) {
    const response = await http.get(`/auth/email/verify/${id}/${hash}`);
    return response.data;
  },

  // Get current user
  async getCurrentUser() {
    const response = await http.get('/auth/user');
    return response.data;
  },

  // Update user profile
  async updateProfile(profileData) {
    const response = await http.put('/auth/profile', profileData);
    return response.data;
  },

  // Change password
  async changePassword(passwordData) {
    const response = await http.put('/auth/password', passwordData);
    return response.data;
  },

  // Token management
  setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
  },

  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  removeToken() {
    localStorage.removeItem(TOKEN_KEY);
  },

  // Check if user is authenticated
  isAuthenticated() {
    return !!this.getToken();
  }
};
