<template>
  <footer class="footer">
    <div class="container-fluid">
      <div class="row align-items-center justify-content-between">
        <div class="col-md-6">
          <div class="footer-text">
            &copy; {{ currentYear }} Go-Vue Code. جميع الحقوق محفوظة.
          </div>
        </div>
        <div class="col-md-6">
          <div class="footer-links text-md-end">
            <a href="#" class="footer-link">سياسة الخصوصية</a>
            <a href="#" class="footer-link">شروط الاستخدام</a>
            <a href="#" class="footer-link">الدعم</a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
  computed: {
    currentYear() {
      return new Date().getFullYear();
    }
  }
};
</script>

<style scoped>
.footer {
  background-color: var(--card-bg);
  border-top: 1px solid var(--border-color);
  padding: 1rem 0;
  font-size: 0.875rem;
  color: var(--text-muted);
}

.footer-link {
  color: var(--text-muted);
  text-decoration: none;
  margin-right: 1rem;
  transition: color 0.3s ease;
}

.footer-link:hover {
  color: var(--primary-color);
}

[dir="rtl"] .footer-link {
  margin-right: 0;
  margin-left: 1rem;
}
</style>
