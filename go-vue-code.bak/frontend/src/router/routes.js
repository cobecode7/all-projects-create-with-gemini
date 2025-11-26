import { useAuthStore } from '@/stores/auth';

// Layouts
import MainLayout from '@/layouts/MainLayout.vue';
import AuthLayout from '@/layouts/AuthLayout.vue';
import ErrorLayout from '@/layouts/ErrorLayout.vue';

// Views
import Dashboard from '@/views/Dashboard.vue';
import Login from '@/views/auth/Login.vue';
import Register from '@/views/auth/Register.vue';
import ForgotPassword from '@/views/auth/ForgotPassword.vue';
import ResetPassword from '@/views/auth/ResetPassword.vue';
import VerifyEmail from '@/views/auth/VerifyEmail.vue';
import Profile from '@/views/Profile.vue';
import Settings from '@/views/Settings.vue';
import Reports from '@/views/Reports.vue';
import UsersList from '@/views/admin/users/UsersList.vue';
import CreateUser from '@/views/admin/users/CreateUser.vue';
import EditUser from '@/views/admin/users/EditUser.vue';
import RolesList from '@/views/admin/roles/RolesList.vue';
import CreateRole from '@/views/admin/roles/CreateRole.vue';
import EditRole from '@/views/admin/roles/EditRole.vue';
import PermissionsList from '@/views/admin/permissions/PermissionsList.vue';
import CreatePermission from '@/views/admin/permissions/CreatePermission.vue';
import EditPermission from '@/views/admin/permissions/EditPermission.vue';
import NotFound from '@/views/errors/NotFound.vue';
import Forbidden from '@/views/errors/Forbidden.vue';
import ServerError from '@/views/errors/ServerError.vue';

export const routes = [
  {
    path: '/',
    redirect: '/dashboard',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { 
          title: 'Dashboard',
          permissions: ['dashboard.view']
        }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: Profile,
        meta: { 
          title: 'Profile'
        }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: Settings,
        meta: { 
          title: 'Settings',
          permissions: ['settings.view']
        }
      },
      {
        path: 'reports',
        name: 'Reports',
        component: Reports,
        meta: { 
          title: 'Reports',
          permissions: ['reports.view']
        }
      },
      {
        path: 'admin',
        meta: { 
          title: 'Admin',
          permissions: ['admin.access']
        },
        children: [
          {
            path: 'users',
            name: 'UsersList',
            component: UsersList,
            meta: { 
              title: 'Users',
              permissions: ['users.view']
            }
          },
          {
            path: 'users/create',
            name: 'CreateUser',
            component: CreateUser,
            meta: { 
              title: 'Create User',
              permissions: ['users.create']
            }
          },
          {
            path: 'users/:id/edit',
            name: 'EditUser',
            component: EditUser,
            meta: { 
              title: 'Edit User',
              permissions: ['users.update']
            },
            props: true
          },
          {
            path: 'roles',
            name: 'RolesList',
            component: RolesList,
            meta: { 
              title: 'Roles',
              permissions: ['roles.view']
            }
          },
          {
            path: 'roles/create',
            name: 'CreateRole',
            component: CreateRole,
            meta: { 
              title: 'Create Role',
              permissions: ['roles.create']
            }
          },
          {
            path: 'roles/:id/edit',
            name: 'EditRole',
            component: EditRole,
            meta: { 
              title: 'Edit Role',
              permissions: ['roles.update']
            },
            props: true
          },
          {
            path: 'permissions',
            name: 'PermissionsList',
            component: PermissionsList,
            meta: { 
              title: 'Permissions',
              permissions: ['permissions.view']
            }
          },
          {
            path: 'permissions/create',
            name: 'CreatePermission',
            component: CreatePermission,
            meta: { 
              title: 'Create Permission',
              permissions: ['permissions.create']
            }
          },
          {
            path: 'permissions/:id/edit',
            name: 'EditPermission',
            component: EditPermission,
            meta: { 
              title: 'Edit Permission',
              permissions: ['permissions.update']
            },
            props: true
          }
        ]
      }
    ]
  },
  {
    path: '/auth',
    component: AuthLayout,
    redirect: '/auth/login',
    meta: { requiresGuest: true },
    children: [
      {
        path: 'login',
        name: 'Login',
        component: Login,
        meta: { 
          title: 'Login'
        }
      },
      {
        path: 'register',
        name: 'Register',
        component: Register,
        meta: { 
          title: 'Register'
        }
      },
      {
        path: 'forgot-password',
        name: 'ForgotPassword',
        component: ForgotPassword,
        meta: { 
          title: 'Forgot Password'
        }
      },
      {
        path: 'reset-password',
        name: 'ResetPassword',
        component: ResetPassword,
        meta: { 
          title: 'Reset Password'
        }
      },
      {
        path: 'verify-email',
        name: 'VerifyEmail',
        component: VerifyEmail,
        meta: { 
          title: 'Verify Email'
        }
      }
    ]
  },
  {
    path: '/error',
    component: ErrorLayout,
    children: [
      {
        path: '404',
        name: 'NotFound',
        component: NotFound,
        meta: { 
          title: 'Page Not Found'
        }
      },
      {
        path: '403',
        name: 'Forbidden',
        component: Forbidden,
        meta: { 
          title: 'Access Denied'
        }
      },
      {
        path: '500',
        name: 'ServerError',
        component: ServerError,
        meta: { 
          title: 'Server Error'
        }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/error/404'
  }
];
