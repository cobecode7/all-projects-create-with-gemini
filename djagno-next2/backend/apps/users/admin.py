from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, UserAddress


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    إعدادات مشرف نموذج المستخدم
    """
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified', 'country')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('معلومات شخصية'), {'fields': ('username', 'first_name', 'last_name', 'phone', 'birth_date', 'avatar')}),
        (_'معلومات الموقع', {'fields': ('country', 'city', 'address', 'postal_code')}),
        (_'الصلاحيات', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        (_'مواعيد مهمة', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    إعدادات مشرف نموذج ملف تعريف المستخدم
    """
    list_display = ('user', 'newsletter_subscribed', 'email_notifications')
    list_filter = ('newsletter_subscribed', 'sms_notifications', 'email_notifications', 'push_notifications')
    search_fields = ('user__email', 'user__username')
    filter_horizontal = ()


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    """
    إعدادات مشرف نموذج عناوين المستخدم
    """
    list_display = ('user', 'title', 'address_type', 'city', 'country', 'is_default')
    list_filter = ('address_type', 'is_default', 'country')
    search_fields = ('user__email', 'user__username', 'title', 'city')
    filter_horizontal = ()
