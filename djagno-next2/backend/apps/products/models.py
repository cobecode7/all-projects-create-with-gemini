from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from django_countries.fields import CountryField


class Category(MPTTModel):
    """
    نموذج الفئات للمنتجات
    """
    name = models.CharField(_'اسم الفئة', max_length=100, unique=True)
    slug = models.SlugField(_'الرابط', max_length=100, unique=True)
    description = models.TextField(_'الوصف', blank=True)
    image = models.ImageField(_'صورة الفئة', upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(_'نشط', default=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(_'تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField(_'تاريخ التحديث', auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _'فئة'
        verbose_name_plural = _'الفئات'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category_detail', args=[self.slug])


class Brand(models.Model):
    """
    نموذج العلامات التجارية
    """
    name = models.CharField(_'اسم العلامة التجارية', max_length=100, unique=True)
    slug = models.SlugField(_'الرابط', max_length=100, unique=True)
    description = models.TextField(_'الوصف', blank=True)
    image = models.ImageField(_'شعار العلامة التجارية', upload_to='brands/', blank=True, null=True)
    is_active = models.BooleanField(_'نشط', default=True)
    country_of_origin = CountryField(_'بلد المنشأ', blank=True, null=True)
    created_at = models.DateTimeField(_'تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField(_'تاريخ التحديث', auto_now=True)

    class Meta:
        verbose_name = _'علامة تجارية'
        verbose_name_plural = _'العلامات التجارية'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:brand_detail', args=[self.slug])


class Product(models.Model):
    """
    نموذج المنتجات
    """
    CONDITION_CHOICES = (
        ('new', _'جديد'),
        ('used', _'مستعمل'),
        ('refurbished', _'مجدّد'),
    )

    name = models.CharField(_'اسم المنتج', max_length=200)
    slug = models.SlugField(_'الرابط', max_length=200, unique=True)
    description = models.TextField(_'الوصف')
    short_description = models.CharField(_'وصف قصير', max_length=500, blank=True)
    sku = models.CharField(_'رمز المنتج', max_length=50, unique=True)
    condition = models.CharField(_'الحالة', max_length=20, choices=CONDITION_CHOICES, default='new')
    category = TreeForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    is_active = models.BooleanField(_'نشط', default=True)
    is_featured = models.BooleanField(_'مميز', default=False)
    is_digital = models.BooleanField(_'منتج رقمي', default=False)
    track_inventory = models.BooleanField(_'تتبع المخزون', default=True)
    created_at = models.DateTimeField(_'تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField(_'تاريخ التحديث', auto_now=True)

    class Meta:
        verbose_name = _'منتج'
        verbose_name_plural = _'المنتجات'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])

    @property
    def in_stock(self):
        """
        التحقق من توفر المنتج في المخزون
        """
        if not self.track_inventory:
            return True
        return self.total_inventory > 0

    @property
    def total_inventory(self):
        """
        حساب إجمالي المخزون المتاح
        """
        return sum(variant.inventory for variant in self.variants.all() if variant.is_active)

    @property
    def min_price(self):
        """
        الحصول على أقل سعر للمنتج
        """
        active_variants = self.variants.filter(is_active=True)
        if active_variants.exists():
            return min(variant.price for variant in active_variants)
        return 0

    @property
    def max_price(self):
        """
        الحصول على أعلى سعر للمنتج
        """
        active_variants = self.variants.filter(is_active=True)
        if active_variants.exists():
            return max(variant.price for variant in active_variants)
        return 0

    @property
    def main_image(self):
        """
        الحصول على الصورة الرئيسية للمنتج
        """
        main_image = self.images.filter(is_main=True).first()
        if main_image:
            return main_image.image
        return self.images.first().image if self.images.exists() else None

    @property
    def average_rating(self):
        """
        حساب متوسط تقييمات المنتج
        """
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    @property
    def review_count(self):
        """
        عدد مراجعات المنتج
        """
        return self.reviews.count()


class ProductVariant(models.Model):
    """
    نموذج متغيرات المنتج (الألوان، الأحجام، إلخ)
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(_'اسم المتغير', max_length=100)
    sku = models.CharField(_'رمز المتغير', max_length=50, unique=True)
    price = models.DecimalField(_'السعر', max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(_'سعر المقارنة', max_digits=10, decimal_places=2, blank=True, null=True)
    cost_per_item = models.DecimalField(_'التكلفة', max_digits=10, decimal_places=2, blank=True, null=True)
    inventory = models.IntegerField(_'المخزون', default=0)
    inventory_policy = models.CharField(_'سياسة المخزون', max_length=20, choices=(
        ('deny', _'رفض'), ('continue', _'متابعة')), default='deny')
    weight = models.DecimalField(_'الوزن', max_digits=8, decimal_places=2, blank=True, null=True)
    barcode = models.CharField(_'الباركود', max_length=50, blank=True, null=True)
    image = models.ImageField(_'صورة المتغير', upload_to='products/variants/', blank=True, null=True)
    is_active = models.BooleanField(_'نشط', default=True)
    created_at = models.DateTimeField(_'تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField(_'تاريخ التحديث', auto_now=True)

    class Meta:
        verbose_name = _'متغير المنتج'
        verbose_name_plural = _'متغيرات المنتج'
        ordering = ['name']

    def __str__(self):
        return f'{self.product.name} - {self.name}'

    @property
    def is_in_stock(self):
        """
        التحقق من توفر المتغير في المخزون
        """
        return self.inventory > 0

    @property
    def discount_percentage(self):
        """
        حساب نسبة الخصم
        """
        if self.compare_price and self.compare_price > self.price:
            return round((self.compare_price - self.price) / self.compare_price * 100, 2)
        return 0


class ProductAttribute(models.Model):
    """
    نموذج خصائص المنتج (اللون، الحجم، المادة، إلخ)
    """
    name = models.CharField(_'اسم الخاصية', max_length=100)
    created_at = models.DateTimeField(_'تاريخ الإنشاء', auto_now_add=True)

    class Meta:
        verbose_name = _'خاصية المنتج'
        verbose_name_plural = _'خصائص المنتج'

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    """
    نموذج قيم خصائص المنتج
    """
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(_'القيمة', max_length=100)
    created_at = models.DateTimeField(_'تاريخ الإنشاء', auto_now_add=True)

    class Meta:
        verbose_name = _'قيمة الخاصية'
        verbose_name_plural = _'قيم الخصائص'
        unique_together = ('attribute', 'value')

    def __str__(self):
        return f'{self.attribute.name}: {self.value}'


class ProductVariantAttribute(models.Model):
    """
    نموذج ربط متغيرات المنتج بخصائصها
    """
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='attributes')
    attribute_value = models.ForeignKey(ProductAttributeValue, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _'خاصية متغير المنتج'
        verbose_name_plural = _'خصائص متغيرات المنتج'
        unique_together = ('variant', 'attribute_value')

    def __str__(self):
        return f'{self.variant.name} - {self.attribute_value}'


class ProductImage(models.Model):
    """
    نموذج صور المنتج
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_'الصورة', upload_to='products/')
    alt_text = models.CharField(_'النص البديل', max_length=200, blank=True)
    is_main = models.BooleanField(_'صورة رئيسية', default=False)
    created_at = models.DateTimeField(_'تاريخ الإنشاء', auto_now_add=True)

    class Meta:
        verbose_name = _'صورة المنتج'
        verbose_name_plural = _'صور المنتج'

    def __str__(self):
        return f'{self.product.name} - {self.id}'


class ProductReview(models.Model):
    """
    نموذج مراجعات المنتج
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(_'التقييم', choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(_'العنوان', max_length=100)
    content = models.TextField(_'المحتوى')
    is_verified_purchase = models.BooleanField(_'شراء مؤكد', default=False)
    is_approved = models.BooleanField(_'موافق عليه', default=False)
    created_at = models.DateTimeField(_'تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField(_'تاريخ التحديث', auto_now=True)

    class Meta:
        verbose_name = _'مراجعة المنتج'
        verbose_name_plural = _'مراجعات المنتج'
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.product.name} - {self.user.username}'


class ProductTag(models.Model):
    """
    نموذج علامات المنتج
    """
    name = models.CharField(_'اسم العلامة', max_length=50, unique=True)
    slug = models.SlugField(_'الرابط', max_length=50, unique=True)
    created_at = models.DateTimeField(_'تاريخ الإنشاء', auto_now_add=True)

    class Meta:
        verbose_name = _'علامة المنتج'
        verbose_name_plural = _'علامات المنتج'

    def __str__(self):
        return self.name


class ProductTagRelation(models.Model):
    """
    نموذج ربط المنتجات بالعلامات
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(ProductTag, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(_'تاريخ الإنشاء', auto_now_add=True)

    class Meta:
        verbose_name = _'علامة المنتج'
        verbose_name_plural = _'علامات المنتج'
        unique_together = ('product', 'tag')

    def __str__(self):
        return f'{self.product.name} - {self.tag.name}' ('product', 'tag')

    def __str__(self):
        return f'{self.product.name} - {self.tag.name}'


class ProductWishlist(models.Model):
    """
    نموذج قائمة رغبات المستخدم
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(_'تاريخ الإضافة', auto_now_add=True)

    class Meta:
        verbose_name = _'منتج في قائمة الرغبات'
        verbose_name_plural = _'قائمة الرغبات'
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'
