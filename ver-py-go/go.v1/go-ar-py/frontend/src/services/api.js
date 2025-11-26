import axios from 'axios';

// إنشاء مثيل من axios مع الإعدادات الأساسية
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8080',
  headers: {
    'Content-Type': 'application/json',
  },
});

// اعتراض الاستجابة للتعامل مع الأخطاء
api.interceptors.response.use(
  response => response,
  error => {
    // في حالة انتهاء صلاحية التوكن
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      delete api.defaults.headers.common['Authorization'];
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;