<template>
  <div class="user-edit">
    <div class="page-header">
      <h2>تعديل المستخدم</h2>
    </div>

    <div class="card">
      <div class="card-body">
        <form @submit.prevent="updateUser">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="firstName" class="form-label">الاسم الأول</label>
              <input type="text" class="form-control" id="firstName" v-model="user.firstName" required>
              <div class="invalid-feedback" v-if="errors.firstName">
                {{ errors.firstName[0] }}
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <label for="lastName" class="form-label">الاسم الأخير</label>
              <input type="text" class="form-control" id="lastName" v-model="user.lastName" required>
              <div class="invalid-feedback" v-if="errors.lastName">
                {{ errors.lastName[0] }}
              </div>
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="email" class="form-label">البريد الإلكتروني</label>
              <input type="email" class="form-control" id="email" v-model="user.email" required>
              <div class="invalid-feedback" v-if="errors.email">
                {{ errors.email[0] }}
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <label for="phone" class="form-label">رقم الهاتف</label>
              <input type="tel" class="form-control" id="phone" v-model="user.phone">
              <div class="invalid-feedback" v-if="errors.phone">
                {{ errors.phone[0] }}
              </div>
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="roleId" class="form-label">الدور</label>
              <select class="form-select" id="roleId" v-model="user.roleId" required>
                <option value="" disabled>اختر دوراً</option>
                <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
              </select>
              <div class="invalid-feedback" v-if="errors.roleId">
                {{ errors.roleId[0] }}
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">الحالة</label>
              <div class="form-check form-switch mt-2">
                <input class="form-check-input" type="checkbox" id="isActive" v-model="user.isActive">
                <label class="form-check-label" for="isActive">نشط</label>
              </div>
            </div>
          </div>

          <div class="mb-3">
            <label for="address" class="form-label">العنوان</label>
            <textarea class="form-control" id="address" rows="3" v-model="user.address"></textarea>
            <div class="invalid-feedback" v-if="errors.address">
              {{ errors.address[0] }}
            </div>
          </div>

          <div class="mb-3">
            <label for="notes" class="form-label">ملاحظات</label>
            <textarea class="form-control" id="notes" rows="3" v-model="user.notes"></textarea>
          </div>

          <!-- Password Reset Section -->
          <div class="card mb-4">
            <div class="card-header">
              <h5>إعادة تعيين كلمة المرور</h5>
            </div>
            <div class="card-body">
              <div class="form-check mb-3">
                <input class="form-check-input" type="checkbox" id="resetPassword" v-model="resetPassword">
                <label class="form-check-label" for="resetPassword">إعادة تعيين كلمة المرور</label>
              </div>

              <div v-if="resetPassword">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="newPassword" class="form-label">كلمة المرور الجديدة</label>
                    <div class="input-group">
                      <input :type="showNewPassword ? 'text' : 'password'" class="form-control" id="newPassword" v-model="newPassword">
                      <button class="btn btn-outline-secondary" type="button" @click="showNewPassword = !showNewPassword">
                        <i :class="showNewPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                      </button>
                    </div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="passwordConfirmation" class="form-label">تأكيد كلمة المرور</label>
                    <div class="input-group">
                      <input :type="showConfirmPassword ? 'text' : 'password'" class="form-control" id="passwordConfirmation" v-model="passwordConfirmation">
                      <button class="btn btn-outline-secondary" type="button" @click="showConfirmPassword = !showConfirmPassword">
                        <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                      </button>
                    </div>
                  </div>
                </div>

                <div class="form-check mb-3">
                  <input class="form-check-input" type="checkbox" id="sendPasswordResetEmail" v-model="sendPasswordResetEmail">
                  <label class="form-check-label" for="sendPasswordResetEmail">إرسال إشعار إعادة تعيين كلمة المرور عبر البريد الإلكتروني</label>
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
  name: 'UserEdit',
  data() {
    return {
      user: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        roleId: '',
        isActive: true,
        address: '',
        notes: ''
      },
      roles: [],
      errors: {},
      loading: false,
      resetPassword: false,
      newPassword: '',
      passwordConfirmation: '',
      showNewPassword: false,
      showConfirmPassword: false,
      sendPasswordResetEmail: true
    };
  },
  created() {
    this.fetchUser();
    this.fetchRoles();
  },
  methods: {
    async fetchUser() {
      try {
        const userId = this.$route.params.id;
        this.user = await adminService.getUserById(userId);
      } catch (error) {
        console.error('Failed to fetch user:', error);
        this.$toast.error('فشل جلب بيانات المستخدم');
        this.$router.push('/admin/users');
      }
    },
    async fetchRoles() {
      try {
        const response = await adminService.getRoles(1, 100);
        this.roles = response.data;
      } catch (error) {
        console.error('Failed to fetch roles:', error);
      }
    },
    async updateUser() {
      this.loading = true;
      this.errors = {};

      try {
        await adminService.updateUser(this.$route.params.id, this.user);

        // Reset password if requested
        if (this.resetPassword && this.newPassword) {
          await adminService.resetUserPassword(this.$route.params.id, this.newPassword);
        }

        this.$toast.success('تم تحديث بيانات المستخدم بنجاح');
        this.$router.push('/admin/users');
      } catch (error) {
        if (error.response && error.response.status === 422) {
          this.errors = error.response.data.errors;
        } else {
          this.$toast.error('فشل تحديث بيانات المستخدم');
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
  margin-bottom: 1rem;
}
</style>
