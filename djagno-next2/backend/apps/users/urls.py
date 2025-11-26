from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'addresses', views.UserAddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh/', views.RefreshTokenView.as_view(), name='token_refresh'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('reset-password/', views.PasswordResetView.as_view(), name='reset_password'),
    path('reset-password-confirm/', views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]
