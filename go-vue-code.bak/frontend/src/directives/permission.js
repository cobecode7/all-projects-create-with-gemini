import { useAuthStore } from '@/stores/auth';

/**
 * v-permission directive
 * Usage:
 * <button v-permission="'users.create'">Add User</button>
 * <div v-permission="['users.view', 'users.update']">User Details</div>
 */
export default {
  mounted(el, binding) {
    const authStore = useAuthStore();
    const { value } = binding;

    if (value && value instanceof Array && value.length > 0) {
      const hasPermission = value.some(permission => authStore.hasPermission(permission));

      if (!hasPermission) {
        el.parentNode && el.parentNode.removeChild(el);
      }
    } else if (value && typeof value === 'string') {
      if (!authStore.hasPermission(value)) {
        el.parentNode && el.parentNode.removeChild(el);
      }
    }
  },

  updated(el, binding) {
    const authStore = useAuthStore();
    const { value, oldValue } = binding;

    // If permission value hasn't changed, don't do anything
    if (JSON.stringify(value) === JSON.stringify(oldValue)) {
      return;
    }

    if (value && value instanceof Array && value.length > 0) {
      const hasPermission = value.some(permission => authStore.hasPermission(permission));

      if (!hasPermission) {
        el.parentNode && el.parentNode.removeChild(el);
      }
    } else if (value && typeof value === 'string') {
      if (!authStore.hasPermission(value)) {
        el.parentNode && el.parentNode.removeChild(el);
      }
    }
  }
};
