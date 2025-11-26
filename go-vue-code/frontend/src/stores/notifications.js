import { defineStore } from 'pinia';

export const useNotificationsStore = defineStore('notifications', {
  state: () => ({
    notifications: [],
    unreadCount: 0,
    loading: false
  }),

  getters: {
    unreadNotifications: (state) => state.notifications.filter(n => !n.read),
    recentNotifications: (state) => state.notifications.slice(0, 5)
  },

  actions: {
    async fetchNotifications() {
      this.loading = true;
      try {
        // In a real app, this would be an API call
        // const response = await http.get('/notifications');
        // this.notifications = response.data;
        // this.unreadCount = this.unreadNotifications.length;

        // For demo purposes, we'll use mock data
        this.notifications = [
          {
            id: 1,
            title: 'مستخدم جديد',
            message: 'تم تسجيل مستخدم جديد في النظام',
            type: 'info',
            read: false,
            createdAt: new Date().toISOString()
          },
          {
            id: 2,
            title: 'تحديث النظام',
            message: 'تم تحديث النظام إلى الإصدار 2.0.1',
            type: 'success',
            read: true,
            createdAt: new Date(Date.now() - 86400000).toISOString()
          },
          {
            id: 3,
            title: 'تنبيه أمان',
            message: 'تم اكتشاف محاولة تسجيل دخول غير مصرح بها',
            type: 'warning',
            read: false,
            createdAt: new Date(Date.now() - 172800000).toISOString()
          }
        ];
        this.unreadCount = this.unreadNotifications.length;
      } catch (error) {
        console.error('Failed to fetch notifications:', error);
      } finally {
        this.loading = false;
      }
    },

    async markAsRead(notificationId) {
      try {
        // In a real app, this would be an API call
        // await http.put(`/notifications/${notificationId}/read`);

        // For demo purposes, we'll update the local state
        const notification = this.notifications.find(n => n.id === notificationId);
        if (notification) {
          notification.read = true;
          this.unreadCount = this.unreadNotifications.length;
        }
      } catch (error) {
        console.error('Failed to mark notification as read:', error);
      }
    },

    async markAllAsRead() {
      try {
        // In a real app, this would be an API call
        // await http.put('/notifications/read-all');

        // For demo purposes, we'll update the local state
        this.notifications.forEach(notification => {
          notification.read = true;
        });
        this.unreadCount = 0;
      } catch (error) {
        console.error('Failed to mark all notifications as read:', error);
      }
    },

    async deleteNotification(notificationId) {
      try {
        // In a real app, this would be an API call
        // await http.delete(`/notifications/${notificationId}`);

        // For demo purposes, we'll update the local state
        const index = this.notifications.findIndex(n => n.id === notificationId);
        if (index !== -1) {
          const notification = this.notifications[index];
          this.notifications.splice(index, 1);
          if (!notification.read) {
            this.unreadCount--;
          }
        }
      } catch (error) {
        console.error('Failed to delete notification:', error);
      }
    },

    addNotification(notification) {
      this.notifications.unshift({
        id: Date.now(),
        ...notification,
        read: false,
        createdAt: new Date().toISOString()
      });
      this.unreadCount++;
    }
  }
});
