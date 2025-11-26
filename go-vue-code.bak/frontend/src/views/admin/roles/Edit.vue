<template>
  <div class="role-edit">
    <div class="page-header">
      <h2>تعديل الدور</h2>
    </div>

    <div class="card">
      <div class="card-body">
        <form @submit.prevent="updateRole">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="name" class="form-label">اسم الدور</label>
              <input type="text" class="form-control" id="name" v-model="role.name" required>
              <div class="invalid-feedback" v-if="errors.name">
                {{ errors.name[0] }}
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <label for="displayName" class="form-label">الاسم المعروض</label>
              <input type="text" class="form-control" id="displayName" v-model="role.displayName" required>
              <div class="invalid-feedback" v-if="errors.displayName">
                {{ errors.displayName[0] }}
              </div>
            </div>
          </div>

          <div class="mb-3">
            <label for="description" class="form-label">الوصف</label>
            <textarea class="form-control" id="description" rows="3" v-model="role.description"></textarea>
            <div class="invalid-feedback" v-if="errors.description">
              {{ errors.description[0] }}
            </div>
          </div>

          <div class="card mb-4">
            <div class="card-header">
              <h5>الصلاحيات</h5>
            </div>
            <div class="card-body">
              <div v-if="loadingPermissions" class="text-center py-3">
                <div class="spinner-border" role="status">
                  <span class="visually-hidden">جاري التحميل...</span>
                </div>
              </div>
              <div v-else>
                <div class="mb-3">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="selectAll" v-model="selectAll">
                    <label class="form-check-label" for="selectAll">
                      تحديد الكل
                    </label>
                  </div>
                </div>

                <div v-for="(permissionGroup, resource) in permissionGroups" :key="resource" class="mb-4">
                  <h6 class="mb-3">{{ getResourceDisplayName(resource) }}</h6>
                  <div class="row">
                    <div v-for="permission in permissionGroup" :key="permission.id" class="col-md-4 mb-2">
                      <div class="form-check">
                        <input class="form-check-input" type="checkbox" :id="`permission-${permission.id}`" 
                               :value="permission.id" v-model="role.permissions">
                        <label class="form-check-label" :for="`permission-${permission.id}`">
                          {{ getPermissionDisplayName(permission.name) }}
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="d-flex justify-content-end">
            <button type="button" class="btn btn-secondary me-2" @click="$router.go(-1)">إلغاء</button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <div class="spinner-border spinner-border-sm me-2" role="status" v-if="loading">
                <span class="visually-hidden">جاري التحميل...</span>
              </div>
              حفظ التغييرات
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import adminService from '@/services/adminService';

export default {
  name: 'RoleEdit',
  data() {
    return {
      role: {
        name: '',
        displayName: '',
        description: '',
        permissions: []
      },
      permissionGroups: {},
      loadingPermissions: false,
      loading: false,
      errors: {}
    };
  },
  computed: {
    selectAll: {
      get() {
        return this.role.permissions.length === this.getAllPermissions().length;
      },
      set(value) {
        if (value) {
          this.role.permissions = this.getAllPermissions().map(p => p.id);
        } else {
          this.role.permissions = [];
        }
      }
    }
  },
  created() {
    this.fetchRole();
    this.fetchPermissionGroups();
  },
  methods: {
    async fetchRole() {
      try {
        const roleId = this.$route.params.id;
        const roleData = await adminService.getRoleById(roleId);
        this.role = {
          name: roleData.name,
          displayName: roleData.displayName,
          description: roleData.description,
          permissions: roleData.permissions.map(p => p.id)
        };
      } catch (error) {
        console.error('Failed to fetch role:', error);
        this.$toast.error('فشل جلب بيانات الدور');
        this.$router.push('/admin/roles');
      }
    },
    async fetchPermissionGroups() {
      this.loadingPermissions = true;
      try {
        this.permissionGroups = await adminService.getPermissionGroups();
      } catch (error) {
        console.error('Failed to fetch permission groups:', error);
      } finally {
        this.loadingPermissions = false;
      }
    },
    getAllPermissions() {
      const allPermissions = [];
      Object.values(this.permissionGroups).forEach(group => {
        allPermissions.push(...group);
      });
      return allPermissions;
    },
    getResourceDisplayName(resource) {
      const displayNames = {
        'users': 'المستخدمون',
        'roles': 'الأدوار',
        'permissions': 'الصلاحيات',
        'dashboard': 'لوحة التحكم',
        'reports': 'التقارير',
        'settings': 'الإعدادات'
      };
      return displayNames[resource] || resource;
    },
    getPermissionDisplayName(permissionName) {
      const permissionNames = {
        'view': 'عرض',
        'create': 'إنشاء',
        'update': 'تحديث',
        'delete': 'حذف',
        'list': 'عرض القائمة',
        'details': 'عرض التفاصيل'
      };

      // Parse permission name like "users.view"
      const parts = permissionName.split('.');
      if (parts.length === 2) {
        const resource = this.getResourceDisplayName(parts[0]);
        const action = permissionNames[parts[1]] || parts[1];
        return `${action} ${resource}`;
      }

      return permissionName;
    },
    async updateRole() {
      this.loading = true;
      this.errors = {};

      try {
        await adminService.updateRole(this.$route.params.id, this.role);
        this.$toast.success('تم تحديث بيانات الدور بنجاح');
        this.$router.push('/admin/roles');
      } catch (error) {
        if (error.response && error.response.status === 422) {
          this.errors = error.response.data.errors;
        } else {
          this.$toast.error('فشل تحديث بيانات الدور');
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.form-check {
  margin-bottom: 0.5rem;
}
</style>
