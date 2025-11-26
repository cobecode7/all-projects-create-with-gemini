import Vue from 'vue';
import VueRouter from 'vue-router';
import Dashboard from '../views/admin/Dashboard.vue';
import Users from '../views/admin/Users.vue';
import Roles from '../views/admin/Roles.vue';
import Permissions from '../views/admin/Permissions.vue';

Vue.use(VueRouter);

const adminRoutes = [
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: Dashboard,
    meta: { 
      title: 'لوحة تحكم المشرفين',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: Users,
    meta: { 
      title: 'إدارة المستخدمين',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/admin/roles',
    name: 'AdminRoles',
    component: Roles,
    meta: { 
      title: 'إدارة الأدوار',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/admin/permissions',
    name: 'AdminPermissions',
    component: Permissions,
    meta: { 
      title: 'إدارة الصلاحيات',
      requiresAuth: true,
      requiresAdmin: true
    }
  }
];

export default adminRoutes;
