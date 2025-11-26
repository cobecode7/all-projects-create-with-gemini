<template>
  <div class="users-management">
    <div class="page-header">
      <h1>إدارة المستخدمين</h1>
      <button class="btn btn-primary" @click="showCreateModal">
        <i class="fas fa-plus"></i> إضافة مستخدم جديد
      </button>
    </div>

    <div class="card">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>المعرف</th>
                <th>الاسم</th>
                <th>البريد الإلكتروني</th>
                <th>الدور</th>
                <th>الحالة</th>
                <th>الإجراءات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.firstName }} {{ user.lastName }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.role ? user.role.name : '-' }}</td>
                <td>
                  <span :class="['badge', user.active ? 'badge-success' : 'badge-danger']">
                    {{ user.active ? 'نشط' : 'غير نشط' }}
                  </span>
                </td>
                <td>
                  <div class="btn-group">
                    <button class="btn btn-sm btn-info" @click="showEditModal(user)">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-warning" @click="showResetPasswordModal(user)">
                      <i class="fas fa-key"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" @click="deleteUser(user.id)">
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
            @click="fetchUsers(currentPage - 1)"
          >
            السابق
          </button>
          <span>صفحة {{ currentPage }} من {{ totalPages }}</span>
          <button 
            class="btn btn-outline-primary" 
            :disabled="currentPage === totalPages" 
            @click="fetchUsers(currentPage + 1)"
          >
            التالي
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit User Modal -->
    <div class="modal" :class="{ 'd-block': showModal }" v-if="showModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ editMode ? 'تعديل مستخدم' : 'إضافة مستخدم جديد' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveUser">
              <div class="mb-3">
                <label for="firstName" class="form-label">الاسم الأول</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="firstName" 
                  v-model="userForm.firstName" 
                  required
                >
              </div>
              <div class="mb-3">
                <label for="lastName" class="form-label">الاسم الأخير</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="lastName" 
                  v-model="userForm.lastName" 
                  required
                >
              </div>
              <div class="mb-3">
                <label for="email" class="form-label">البريد الإلكتروني</label>
                <input 
                  type="email" 
                  class="form-control" 
                  id="email" 
                  v-model="userForm.email" 
                  required
                >
              </div>
              <div class="mb-3" v-if="!editMode">
                <label for="password" class="form-label">كلمة المرور</label>
                <input 
                  type="password" 
                  class="form-control" 
                  id="password" 
                  v-model="userForm.password" 
                  required
                >
              </div>
              <div class="mb-3">
                <label for="roleId" class="form-label">الدور</label>
                <select class="form-select" id="roleId" v-model="userForm.roleId" required>
                  <option value="" disabled>اختر دوراً</option>
                  <option v-for="role in roles" :key="role.id" :value="role.id">
                    {{ role.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3 form-check" v-if="editMode">
                <input 
                  type="checkbox" 
                  class="form-check-input" 
                  id="active" 
                  v-model="userForm.active"
                >
                <label class="form-check-label" for="active">نشط</label>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">إلغاء</button>
            <button type="button" class="btn btn-primary" @click="saveUser">
              {{ editMode ? 'حفظ التغييرات' : 'إضافة المستخدم' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Reset Password Modal -->
    <div class="modal" :class="{ 'd-block': showPasswordModal }" v-if="showPasswordModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">إعادة تعيين كلمة المرور</h5>
            <button type="button" class="btn-close" @click="closePasswordModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="resetPassword">
              <div class="mb-3">
                <label for="newPassword" class="form-label">كلمة المرور الجديدة</label>
                <input 
                  type="password" 
                  class="form-control" 
                  id="newPassword" 
                  v-model="passwordForm.newPassword" 
                  required
                >
              </div>
              <div class="mb-3">
                <label for="confirmPassword" class="form-label">تأكيد كلمة المرور</label>
                <input 
                  type="password" 
                  class="form-control" 
                  id="confirmPassword" 
                  v-model="passwordForm.confirmPassword" 
                  required
                >
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closePasswordModal">إلغاء</button>
            <button type="button" class="btn btn-primary" @click="resetPassword">
              إعادة تعيين كلمة المرور
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
  name: 'UsersManagement',
  data() {
    return {
      users: [],
      roles: [],
      currentPage: 1,
      totalPages: 1,
      showModal: false,
      showPasswordModal: false,
      editMode: false,
      userForm: {
        id: null,
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        roleId: null,
        active: true
      },
      passwordForm: {
        id: null,
        newPassword: '',
        confirmPassword: ''
      }
    };
  },
  created() {
    this.fetchUsers();
    this.fetchRoles();
  },
  methods: {
    async fetchUsers(page = 1) {
      try {
        const response = await axios.get(`/api/admin/users?page=${page}&limit=10`);
        this.users = response.data.users;
        this.currentPage = response.data.page;
        this.totalPages = Math.ceil(response.data.total / response.data.limit);
      } catch (error) {
        console.error('Error fetching users:', error);
        this.$toast.error('فشل في جلب المستخدمين');
      }
    },
    async fetchRoles() {
      try {
        const response = await axios.get('/api/admin/roles');
        this.roles = response.data.roles;
      } catch (error) {
        console.error('Error fetching roles:', error);
        this.$toast.error('فشل في جلب الأدوار');
      }
    },
    showCreateModal() {
      this.editMode = false;
      this.userForm = {
        id: null,
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        roleId: null,
        active: true
      };
      this.showModal = true;
    },
    showEditModal(user) {
      this.editMode = true;
      this.userForm = {
        id: user.id,
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        password: '',
        roleId: user.roleId,
        active: user.active
      };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    async saveUser() {
      try {
        if (this.editMode) {
          await axios.put(`/api/admin/users/${this.userForm.id}`, this.userForm);
          this.$toast.success('تم تحديث المستخدم بنجاح');
        } else {
          await axios.post('/api/admin/users', this.userForm);
          this.$toast.success('تم إضافة المستخدم بنجاح');
        }
        this.closeModal();
        this.fetchUsers(this.currentPage);
      } catch (error) {
        console.error('Error saving user:', error);
        this.$toast.error('فشل في حفظ المستخدم');
      }
    },
    showResetPasswordModal(user) {
      this.passwordForm = {
        id: user.id,
        newPassword: '',
        confirmPassword: ''
      };
      this.showPasswordModal = true;
    },
    closePasswordModal() {
      this.showPasswordModal = false;
    },
    async resetPassword() {
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        this.$toast.error('كلمات المرور غير متطابقة');
        return;
      }

      try {
        await axios.post(`/api/admin/users/${this.passwordForm.id}/reset-password`, {
          newPassword: this.passwordForm.newPassword
        });
        this.$toast.success('تم إعادة تعيين كلمة المرور بنجاح');
        this.closePasswordModal();
      } catch (error) {
        console.error('Error resetting password:', error);
        this.$toast.error('فشل في إعادة تعيين كلمة المرور');
      }
    },
    async deleteUser(userId) {
      if (!confirm('هل أنت متأكد من أنك تريد حذف هذا المستخدم؟')) {
        return;
      }

      try {
        await axios.delete(`/api/admin/users/${userId}`);
        this.$toast.success('تم حذف المستخدم بنجاح');
        this.fetchUsers(this.currentPage);
      } catch (error) {
        console.error('Error deleting user:', error);
        this.$toast.error('فشل في حذف المستخدم');
      }
    }
  }
};
</script>

<style scoped>
.users-management {
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

.badge {
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
}

.badge-success {
  background-color: #28a745;
  color: white;
}

.badge-danger {
  background-color: #dc3545;
  color: white;
}

.btn-group {
  display: flex;
  gap: 5px;
}
</style>
