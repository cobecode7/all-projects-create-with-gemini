<template>
  <div class="user-create">
    <div class="page-header">
      <h2>إضافة مستخدم جديد</h2>
    </div>

    <div class="card">
      <div class="card-body">
        <form @submit.prevent="createUser">
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
              <label for="password" class="form-label">كلمة المرور</label>
              <div class="input-group">
                <input :type="showPassword ? 'text' : 'password'" class="form-control" id="password" v-model="user.password" required>
                <button class="btn btn-outline-secondary" type="button" @click="showPassword = !showPassword">
                  <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
              <div class="invalid-feedback" v-if="errors.password">
                {{ errors.password[0] }}
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <label for="passwordConfirmation" class="form-label">تأكيد كلمة المرور</label>
              <div class="input-group">
                <input :type="showConfirmPassword ? 'text' : 'password'" class="form-control" id="passwordConfirmation" v-model="user.passwordConfirmation" required>
                <button class="btn btn-outline-secondary" type="button" @click="showConfirmPassword = !showConfirmPassword">
                  <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
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

          <div class="mb-3 form-check">
            <input type="checkbox" class="form-check-input" id="sendWelcomeEmail" v-model="sendWelcomeEmail">
            <label class="form-check-label" for="sendWelcomeEmail">إرسال بريد إلكتروني ترحيبي</label>
          </div>

          <div class="mb-3">
            <label for="notes" class="form-label">ملاحظات</label>
            <textarea class="form-control" id="notes" rows="3" v-model="user.notes"></textarea>
          </div>

          <div class="d-flex justify-content-end">
            <button type="button" class="btn btn-secondary me-2" @click="$router.go(-1)">إلغاء</button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <div class="spinner-border spinner-border-sm me-2" role="status" v-if="loading">
                <span class="visually-hidden">جاري التحميل...</span>
              </div>
              حفظ
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
  name: 'UserCreate',
  data() {
    return {
      user: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        password: '',
        passwordConfirmation: '',
        roleId: '',
        isActive: true,
        address: '',
        notes: ''
      },
      roles: [],
      errors: {},
      loading: false,
      showPassword: false,
      showConfirmPassword: false,
      sendWelcomeEmail: true
    };
  },
  created() {
    this.fetchRoles();
  },
  methods: {
    async fetchRoles() {
      try {
        const response = await adminService.getRoles(1, 100);
        this.roles = response.data;
      } catch (error) {
        console.error('Failed to fetch roles:', error);
      }
    },
    async createUser() {
      this.loading = true;
      this.errors = {};

      try {
        const response = await adminService.createUser({
          ...this.user,
          sendWelcomeEmail: this.sendWelcomeEmail
        });

        this.$toast.success('تم إضافة المستخدم بنجاح');
        this.$router.push('/admin/users');
      } catch (error) {
        if (error.response && error.response.status === 422) {
          this.errors = error.response.data.errors;
        } else {
          this.$toast.error('فشل إضافة المستخدم');
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
