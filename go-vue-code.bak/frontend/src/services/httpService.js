import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useToast } from 'vue-toastification';

// Create axios instance
const http = axios.create({
  baseURL: process.env.VUE_APP_API_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
http.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
http.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const toast = useToast();
    const authStore = useAuthStore();

    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      const { status, data } = error.response;

      if (status === 401) {
        // Unauthorized - token expired or invalid
        authStore.logout();
        toast.error('انتهت صلاحية الجلسة، يرجى تسجيل الدخول مرة أخرى');
        window.location.href = '/login';
      } else if (status === 403) {
        // Forbidden - user doesn't have permission
        toast.error('ليس لديك صلاحية للوصول إلى هذه الصفحة');
      } else if (status === 404) {
        // Not found
        toast.error('الصفحة المطلوبة غير موجودة');
      } else if (status >= 500) {
        // Server error
        toast.error('حدث خطأ في الخادم، يرجى المحاولة مرة أخرى');
      } else {
        // Other errors
        toast.error(data.error || 'حدث خطأ ما');
      }
    } else if (error.request) {
      // The request was made but no response was received
      toast.error('لا يمكن الاتصال بالخادم، يرجى التحقق من اتصالك بالإنترنت');
    } else {
      // Something happened in setting up the request that triggered an Error
      toast.error('حدث خطأ ما، يرجى المحاولة مرة أخرى');
    }

    return Promise.reject(error);
  }
);

export default http;
