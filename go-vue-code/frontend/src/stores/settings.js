import { defineStore } from 'pinia';
import adminService from '@/services/adminService';

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    settings: {},
    loading: false,
    theme: localStorage.getItem('theme') || 'light',
    language: localStorage.getItem('language') || 'ar',
    sidebarCollapsed: localStorage.getItem('sidebarCollapsed') === 'true'
  }),

  getters: {
    getSetting: (state) => (key) => {
      return state.settings[key] || null;
    },

    isDarkTheme: (state) => state.theme === 'dark',

    isRTL: (state) => state.language === 'ar'
  },

  actions: {
    async fetchSettings() {
      this.loading = true;
      try {
        const response = await adminService.getSettings();
        this.settings = response;
      } catch (error) {
        console.error('Failed to fetch settings:', error);
      } finally {
        this.loading = false;
      }
    },

    async updateSettings(settingsData) {
      this.loading = true;
      try {
        const response = await adminService.updateSettings(settingsData);
        this.settings = { ...this.settings, ...response };
        return response;
      } catch (error) {
        console.error('Failed to update settings:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    setTheme(theme) {
      this.theme = theme;
      localStorage.setItem('theme', theme);
      document.documentElement.setAttribute('data-theme', theme);
    },

    toggleTheme() {
      this.setTheme(this.theme === 'light' ? 'dark' : 'light');
    },

    setLanguage(language) {
      this.language = language;
      localStorage.setItem('language', language);
      document.documentElement.setAttribute('lang', language);
      document.documentElement.setAttribute('dir', language === 'ar' ? 'rtl' : 'ltr');
    },

    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
      localStorage.setItem('sidebarCollapsed', this.sidebarCollapsed.toString());
    },

    setSidebarCollapsed(collapsed) {
      this.sidebarCollapsed = collapsed;
      localStorage.setItem('sidebarCollapsed', collapsed.toString());
    }
  }
});
