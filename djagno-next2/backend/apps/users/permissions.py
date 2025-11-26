from rest_framework import permissions
from django.utils.translation import gettext_lazy as _


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    صلاحية تسمح فقط لأصحاب الكائن بتعديله
    """
    def has_object_permission(self, request, view, obj):
        # عمليات القراءة مسموحة لأي طلب
        if request.method in permissions.SAFE_METHODS:
            return True
        # عمليات الكتابة مسموحة فقط لصاحب الكائن
        return obj.user == request.user


class IsAdminOrOwner(permissions.BasePermission):
    """
    صلاحية تسمح فقط للمشرفين أو أصحاب الكائن بالوصول
    """
    def has_object_permission(self, request, view, obj):
        # المشرفون يمكنهم الوصول إلى أي كائن
        if request.user.is_staff:
            return True
        # أصحاب الكائن يمكنهم الوصول إلى كائنهم
        return obj.user == request.user


class IsVerifiedUser(permissions.BasePermission):
    """
    صلاحية تسمح فقط للمستخدمين المفعّلين بالوصول
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_verified


class IsVendorOrAdmin(permissions.BasePermission):
    """
    صلاحية تسمح فقط للبائعين أو المشرفين بالوصول
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                (request.user.is_staff or 
                 hasattr(request.user, 'vendor_profile')))
