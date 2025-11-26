<template>
  <div class="permissions-management">
    <div class="page-header">
      <h1>إدارة الصلاحيات</h1>
      <button class="btn btn-primary" @click="showCreateModal">
        <i class="fas fa-plus"></i> إضافة صلاحية جديدة
      </button>
    </div>

    <div class="card">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>المعرف</th>
                <th>اسم الصلاحية</th>
                <th>الوصف</th>
                <th>الإجراءات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="permission in permissions" :key="permission.id">
                <td>{{ permission.id }}</td>
                <td>{{ permission.name }}</td>
                <td>{{ permission.description }}</td>
                <td>
                  <div class="btn-group">
                    <button class="btn btn-sm btn-info" @click="showEditModal(permission)">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" @click="deletePermission(permission.id)">
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
            @click="fetchPermissions(currentPage - 1)"
          >
            السابق
          </button>
          <span>صفحة {{ currentPage }} من {{ totalPages }}</span>
          <button 
            class="btn btn-outline-primary" 
            :disabled="currentPage === totalPages" 
            @click="fetchPermissions(currentPage + 1)"
          >
            التالي
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Permission Modal -->
    <div class="modal" :class="{ 'd-block': showModal }" v-if="showModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ editMode ? 'تعديل صلاحية' : 'إضافة صلاحية جديدة' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="savePermission">
              <div class="mb-3">
                <label for="name" class="form-label">اسم الصلاحية</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="name" 
                  v-model="permissionForm.name" 
                  required
                >
                <small class="form-text text-muted">
                  مثال: users.create, roles.update, permissions.delete
                </small>
              </div>
              <div class="mb-3">
                <label for="description" class="form-label">الوصف</label>
                <textarea 
                  class="form-control" 
                  id="description" 
                  v-model="permissionForm.description" 
                  rows="3"
                ></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">إلغاء</button>
            <button type="button" class="btn btn-primary" @click="savePermission">
              {{ editMode ? 'حفظ التغييرات' : 'إضافة الصلاحية' }}
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
  name: 'PermissionsManagement',
  data() {
    return {
      permissions: [],
      currentPage: 1,
      totalPages: 1,
      showModal: false,
      editMode: false,
      permissionForm: {
        id: null,
        name: '',
        description: ''
      }
    };
  },
  created() {
    this.fetchPermissions();
  },
  methods: {
    async fetchPermissions(page = 1) {
      try {
        const response = await axios.get(`/api/admin/permissions?page=${page}&limit=10`);
        this.permissions = response.data.permissions;
        this.currentPage = response.data.page;
        this.totalPages = Math.ceil(response.data.total / response.data.limit);
      } catch (error) {
        console.error('Error fetching permissions:', error);
        this.$toast.error('فشل في جلب الصلاحيات');
      }
    },
    showCreateModal() {
      this.editMode = false;
      this.permissionForm = {
        id: null,
        name: '',
        description: ''
      };
      this.showModal = true;
    },
    showEditModal(permission) {
      this.editMode = true;
      this.permissionForm = {
        id: permission.id,
        name: permission.name,
        description: permission.description
      };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    async savePermission() {
      try {
        if (this.editMode) {
          await axios.put(`/api/admin/permissions/${this.permissionForm.id}`, this.permissionForm);
          this.$toast.success('تم تحديث الصلاحية بنجاح');
        } else {
          await axios.post('/api/admin/permissions', this.permissionForm);
          this.$toast.success('تم إضافة الصلاحية بنجاح');
        }
        this.closeModal();
        this.fetchPermissions(this.currentPage);
      } catch (error) {
        console.error('Error saving permission:', error);
        this.$toast.error('فشل في حفظ الصلاحية');
      }
    },
    async deletePermission(permissionId) {
      if (!confirm('هل أنت متأكد من أنك تريد حذف هذه الصلاحية؟')) {
        return;
      }

      try {
        await axios.delete(`/api/admin/permissions/${permissionId}`);
        this.$toast.success('تم حذف الصلاحية بنجاح');
        this.fetchPermissions(this.currentPage);
      } catch (error) {
        console.error('Error deleting permission:', error);
        if (error.response && error.response.data && error.response.data.error) {
          this.$toast.error(error.response.data.error);
        } else {
          this.$toast.error('فشل في حذف الصلاحية');
        }
      }
    }
  }
};
</script>

<style scoped>
.permissions-management {
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

.btn-group {
  display: flex;
  gap: 5px;
}
</style>
