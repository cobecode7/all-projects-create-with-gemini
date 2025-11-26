from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class User(AbstractUser):
    """
    نموذج المستخدم المخصص للنظام
    """
    email = models.EmailField(_('البريد الإلكتروني'), unique=True)
    phone = models.CharField(_('رقم الهاتف'), max_length=20, blank=True, null=True)
    birth_date = models.DateField(_('تاريخ الميلاد'), blank=True, null=True)
    avatar = models.ImageField(_('الصورة الشخصية'), upload_to='avatars/', blank=True, null=True)
    country = CountryField(_('الدولة'), blank=True, null=True)
    city = models.CharField(_('المدينة'), max_length=100, blank=True, null=True)
    address = models.TextField(_('العنوان'), blank=True, null=True)
    postal_code = models.CharField(_('الرمز البريدي'), max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(_'حالة التحقق', default=False)
    created_at = models.DateTimeField(_'تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField(_'تاريخ التحديث', auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _'مستخدم'
        verbose_name_plural = _'المستخدمون'

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """
    ملف تعريف المستخدم الإضافي
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(_'السيرة الذاتية', blank=True, null=True)
    website = models.URLField(_'الموقع الإلكتروني', blank=True, null=True)
    social_twitter = models.CharField(_'تويتر', max_length=50, blank=True, null=True)
    social_facebook = models.CharField(_'فيسبوك', max_length=50, blank=True, null=True)
    social_instagram = models.CharField(_'انستغرام', max_length=50, blank=True, null=True)
    social_linkedin = models.CharField(_'لينكدإن', max_length=50, blank=True, null=True)
    newsletter_subscribed = models.BooleanField(_'مشترك في النشرة البريدية', default=False)
    sms_notifications = models.BooleanField(_'إشعارات الرسائل القصيرة', default=True)
    email_notifications = models.BooleanField(_'إشعارات البريد الإلكتروني', default=True)
    push_notifications = models.BooleanField(_'الإشعارات الفورية', default=True)

    class Meta:
        verbose_name = _'ملف تعريف المستخدم'
        verbose_name_plural = _'ملفات تعريف المستخدمين'

    def __str__(self):
        return f'{self.user.username} Profile'


class UserAddress(models.Model):
    """
    عناوين المستخدم
    """
    ADDRESS_TYPES = (
        ('home', _'المنزل'),
        ('work', _'العمل'),
        ('other', _'أخرى'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(_'نوع العنوان', max_length=10, choices=ADDRESS_TYPES, default='home')
    title = models.CharField(_'عنوان التسمية', max_length=100)
    address = models.TextField(_'العنوان')
    city = models.CharField(_'المدينة', max_length=100)
    postal_code = models.CharField(_'الرمز البريدي', max_length=20)
    country = CountryField(_'الدولة')
    is_default = models.BooleanField(_'عنوان افتراضي', default=False)
    created_at = models.DateTimeField(_'تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField(_'تاريخ التحديث', auto_now=True)

    class Meta:
        verbose_name = _'عنوان المستخدم'
        verbose_name_plural = _'عناوين المستخدمين'
        ordering = ['-is_default', 'title']

    def __str__(self):
        return f'{self.user.username} - {self.title}'
