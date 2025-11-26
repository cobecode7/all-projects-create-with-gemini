<template>
  <div class="p-5 mb-4 bg-light rounded-3">
    <div class="container-fluid py-5">
      <h1 class="display-5 fw-bold">مرحباً بك في نظام Go Vue Auth</h1>
      <p class="col-md-8 fs-4">
        نظام مصادقة متكامل مبني باستخدام Go/Gin للواجهة الخلفية و Vue.js 3 للواجهة الأمامية.
        يوفر النظام تسجيل المستخدمين، تسجيل الدخول، إدارة الأدوار والصلاحيات.
      </p>
      <div class="d-grid gap-2 d-md-flex justify-content-md-start">
        <router-link v-if="!isAuthenticated" to="/register" class="btn btn-primary btn-lg px-4 me-md-2">
          إنشاء حساب جديد
        </router-link>
        <router-link v-if="!isAuthenticated" to="/login" class="btn btn-outline-secondary btn-lg px-4">
          تسجيل الدخول
        </router-link>
        <router-link v-if="isAuthenticated" to="/dashboard" class="btn btn-primary btn-lg px-4 me-md-2">
          لوحة التحكم
        </router-link>
      </div>
    </div>
  </div>

  <div class="row align-items-md-stretch">
    <div class="col-md-6">
      <div class="h-100 p-5 text-bg-dark rounded-3">
        <h2>مميزات النظام</h2>
        <p>
          <ul>
            <li>تسجيل المستخدمين الجدد</li>
            <li>تسجيل الدخول والخروج الآمن</li>
            <li>إدارة الأدوار والصلاحيات</li>
            <li>حماية المسارات المطلوبة للمصادقة</li>
            <li>واجهة مستخدم حديثة وسهلة الاستخدام</li>
          </ul>
        </p>
      </div>
    </div>
    <div class="col-md-6">
      <div class="h-100 p-5 bg-light border rounded-3">
        <h2>التقنيات المستخدمة</h2>
        <p>
          <ul>
            <li>Go/Gin Framework للواجهة الخلفية</li>
            <li>PostgreSQL كقاعدة بيانات</li>
            <li>GORM للتعامل مع قاعدة البيانات</li>
            <li>Vue.js 3 للواجهة الأمامية</li>
            <li>JWT للمصادقة</li>
          </ul>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>
