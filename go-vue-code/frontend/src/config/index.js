// App configuration
export default {
  // App info
  name: 'Go-Vue Code',
  version: '1.0.0',
  description: 'نظام إدارة المحتوى',

  // API configuration
  api: {
    baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000/api',
    timeout: 10000
  },

  // Authentication
  auth: {
    tokenKey: 'auth_token',
    refreshTokenKey: 'refresh_token',
    tokenExpiryKey: 'token_expiry'
  },

  // Theme
  theme: {
    defaultTheme: 'light',
    availableThemes: ['light', 'dark']
  },

  // Language
  language: {
    defaultLanguage: 'ar',
    availableLanguages: ['ar', 'en']
  },

  // Pagination
  pagination: {
    defaultPerPage: 10,
    perPageOptions: [5, 10, 20, 50]
  },

  // File upload
  upload: {
    maxFileSize: 5 * 1024 * 1024, // 5MB
    allowedFileTypes: ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'text/plain']
  },

  // Routes
  routes: {
    home: '/',
    login: '/login',
    register: '/register',
    dashboard: '/dashboard',
    admin: '/admin',
    profile: '/profile',
    settings: '/settings'
  },

  // Toast notifications
  toast: {
    position: 'top-right',
    timeout: 3000,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: false,
    closeButton: 'button',
    icon: true,
    rtl: true
  }
};
