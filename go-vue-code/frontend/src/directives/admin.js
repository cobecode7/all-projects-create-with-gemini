import { useAuthStore } from '@/stores/auth';

/**
 * v-admin directive
 * Usage:
 * <button v-admin>Admin Only Button</button>
 */
export default {
  mounted(el, binding) {
    const authStore = useAuthStore();

    if (!authStore.isAdmin) {
      el.parentNode && el.parentNode.removeChild(el);
    }
  },

  updated(el, binding) {
    const authStore = useAuthStore();

    if (!authStore.isAdmin) {
      el.parentNode && el.parentNode.removeChild(el);
    }
  }
};
