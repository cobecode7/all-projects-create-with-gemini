<template>
  <div class="roles-management">
    <div class="page-header">
      <h1>إدارة الأدوار</h1>
      <button class="btn btn-primary" @click="showCreateModal">
        <i class="fas fa-plus"></i> إضافة دور جديد
      </button>
    </div>

    <div class="card">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>المعرف</th>
                <th>اسم الدور</th>
                <th>الوصف</th>
                <th>الصلاحيات</th>
                <th>الإجراءات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="role in roles" :key="role.id">
                <td>{{ role.id }}</td>
                <td>{{ role.name }}</td>
                <td>{{ role.description }}</td>
                <td>
                  <div class="permission-tags">
                    <span 
                      v-for="permission in role.permissions" 
                      :key="permission.id" 
                      class="badge badge-info"
                    >
                      {{ permission.name }}
                    </span>
                  </div>
                </td>
                <td>
                  <div class="btn-group">
                    <button class="btn btn-sm btn-info" @click="showEditModal(role)">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" @click="deleteRole(role.id)">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="pagination">
          <button 
            class="btn btn-outline-primary" 
            :disabled="currentPage === 1" 
            @click="fetchRoles(currentPage - 1)"
          >
            السابق
          </button>
          <span>صفحة {{ currentPage }} من {{ totalPages }}</span>
          <button 
            class="btn btn-outline-primary" 
            :disabled="currentPage === totalPages" 
            @click="fetchRoles(currentPage + 1)"
          >
            التالي
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Role Modal -->
    <div class="modal" :class="{ 'd-block': showModal }" v-if="showModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ editMode ? 'تعديل دور' : 'إضافة دور جديد' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveRole">
              <div class="mb-3">
                <label for="name" class="form-label">اسم الدور</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="name" 
                  v-model="roleForm.name" 
                  required
                >
              </div>
              <div class="mb-3">
                <label for="description" class="form-label">الوصف</label>
                <textarea 
                  class="form-control" 
                  id="description" 
                  v-model="roleForm.description" 
                  rows="3"
                ></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">الصلاحيات</label>
                <div class="permissions-container">
                  <div v-for="(permissions, resource) in permissionGroups" :key="resource" class="permission-group">
                    <h6>{{ getResourceDisplayName(resource) }}</h6>
                    <div class="form-check" v-for="permission in permissions" :key="permission.id">
                      <input 
                        class="form-check-input" 
                        type="checkbox" 
                        :id="`permission-${permission.id}`" 
                        :value="permission.id"
                        v-model="roleForm.permissionIds"
                      >
                      <label class="form-check-label" :for="`permission-${permission.id}`">
                        {{ getPermissionDisplayName(permission.name) }}
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">إلغاء</button>
            <button type="button" class="btn btn-primary" @click="saveRole">
              {{ editMode ? 'حفظ التغييرات' : 'إضافة الدور' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RolesManagement',
  data() {
    return {
      roles: [],
      permissionGroups: {},
      currentPage: 1,
      totalPages: 1,
      showModal: false,
      editMode: false,
      roleForm: {
        id: null,
        name: '',
        description: '',
        permissionIds: []
      }
    };
  },
  created() {
    this.fetchRoles();
    this.fetchPermissionGroups();
  },
  methods: {
    async fetchRoles(page = 1) {
      try {
        const response = await axios.get(`/api/admin/roles?page=${page}&limit=10`);
        this.roles = response.data.roles;
        this.currentPage = response.data.page;
        this.totalPages = Math.ceil(response.data.total / response.data.limit);
      } catch (error) {
        console.error('Error fetching roles:', error);
        this.$toast.error('فشل في جلب الأدوار');
      }
    },
    async fetchPermissionGroups() {
      try {
        const response = await axios.get('/api/admin/permissions/groups');
        this.permissionGroups = response.data;
      } catch (error) {
        console.error('Error fetching permission groups:', error);
        this.$toast.error('فشل في جلب الصلاحيات');
      }
    },
    showCreateModal() {
      this.editMode = false;
      this.roleForm = {
        id: null,
        name: '',
        description: '',
        permissionIds: []
      };
      this.showModal = true;
    },
    showEditModal(role) {
      this.editMode = true;
      this.roleForm = {
        id: role.id,
        name: role.name,
        description: role.description,
        permissionIds: role.permissions.map(p => p.id)
      };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    async saveRole() {
      try {
        if (this.editMode) {
          await axios.put(`/api/admin/roles/${this.roleForm.id}`, this.roleForm);
          this.$toast.success('تم تحديث الدور بنجاح');
        } else {
          await axios.post('/api/admin/roles', this.roleForm);
          this.$toast.success('تم إضافة الدور بنجاح');
        }
        this.closeModal();
        this.fetchRoles(this.currentPage);
      } catch (error) {
        console.error('Error saving role:', error);
        this.$toast.error('فشل في حفظ الدور');
      }
    },
    async deleteRole(roleId) {
      if (!confirm('هل أنت متأكد من أنك تريد حذف هذا الدور؟')) {
        return;
      }

      try {
        await axios.delete(`/api/admin/roles/${roleId}`);
        this.$toast.success('تم حذف الدور بنجاح');
        this.fetchRoles(this.currentPage);
      } catch (error) {
        console.error('Error deleting role:', error);
        if (error.response && error.response.data && error.response.data.error) {
          this.$toast.error(error.response.data.error);
        } else {
          this.$toast.error('فشل في حذف الدور');
        }
      }
    },
    getResourceDisplayName(resource) {
      const resourceNames = {
        'users': 'المستخدمون',
        'roles': 'الأدوار',
        'permissions': 'الصلاحيات'
      };
      return resourceNames[resource] || resource;
    },
    getPermissionDisplayName(permission) {
      const permissionNames = {
        'users.view': 'عرض المستخدمين',
        'users.create': 'إنشاء المستخدمين',
        'users.update': 'تحديث المستخدمين',
        'users.delete': 'حذف المستخدمين',
        'roles.view': 'عرض الأدوار',
        'roles.create': 'إنشاء الأدوار',
        'roles.update': 'تحديث الأدوار',
        'roles.delete': 'حذف الأدوار',
        'permissions.view': 'عرض الصلاحيات',
        'permissions.create': 'إنشاء الصلاحيات',
        'permissions.update': 'تحديث الصلاحيات',
        'permissions.delete': 'حذف الصلاحيات'
      };
      return permissionNames[permission] || permission;
    }
  }
};
</script>

<style scoped>
.roles-management {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

.modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-dialog {
  margin-top: 100px;
}

.permission-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.badge {
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
}

.badge-info {
  background-color: #17a2b8;
  color: white;
}

.btn-group {
  display: flex;
  gap: 5px;
}

.permissions-container {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 5px;
}

.permission-group {
  margin-bottom: 15px;
}

.permission-group h6 {
  margin-bottom: 10px;
  font-weight: bold;
  color: #495057;
}

.form-check {
  margin-bottom: 5px;
}
</style>
