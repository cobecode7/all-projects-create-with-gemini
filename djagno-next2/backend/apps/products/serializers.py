from rest_framework import serializers
from .models import (
    Category, Brand, Product, ProductVariant, ProductAttribute,
    ProductAttributeValue, ProductVariantAttribute, ProductImage,
    ProductReview, ProductTag, ProductTagRelation
)


class CategorySerializer(serializers.ModelSerializer):
    """
    مسلسل بيانات الفئات
    """
    children = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'image', 'is_active',
                  'created_at', 'updated_at', 'children', 'product_count')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_children(self, obj):
        children = obj.get_children()
        return CategorySerializer(children, many=True).data

    def get_product_count(self, obj):
        return obj.get_descendants(include_self=True).filter(products__is_active=True).count()


class BrandSerializer(serializers.ModelSerializer):
    """
    مسلسل بيانات العلامات التجارية
    """
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ('id', 'name', 'slug', 'description', 'image', 'is_active',
                  'country_of_origin', 'created_at', 'updated_at', 'product_count')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    """
    مسلسل بيانات قيم خصائص المنتج
    """
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = ('id', 'attribute', 'attribute_name', 'value')
        read_only_fields = ('id',)


class ProductVariantAttributeSerializer(serializers.ModelSerializer):
    """
    مسلسل بيانات خصائص متغيرات المنتج
    """
    attribute_value = ProductAttributeValueSerializer(read_only=True)

    class Meta:
        model = ProductVariantAttribute
        fields = ('id', 'attribute_value')
        read_only_fields = ('id',)


class ProductVariantSerializer(serializers.ModelSerializer):
    """
    مسلسل بيانات متغيرات المنتج
    """
    attributes = ProductVariantAttributeSerializer(many=True, read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ('id', 'name', 'sku', 'price', 'compare_price', 'cost_per_item',
                  'inventory', 'inventory_policy', 'weight', 'barcode', 'image',
                  'is_active', 'created_at', 'updated_at', 'attributes',
                  'is_in_stock', 'discount_percentage')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProductImageSerializer(serializers.ModelSerializer):
    """
    مسلسل بيانات صور المنتج
    """
    image_url = serializers.ImageField(source='image', read_only=True)

    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'image_url', 'alt_text', 'is_main', 'created_at')
        read_only_fields = ('id', 'created_at')


class ProductReviewSerializer(serializers.ModelSerializer):
    """
    مسلسل بيانات مراجعات المنتج
    """
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)

    class Meta:
        model = ProductReview
        fields = ('id', 'product', 'user', 'user_name', 'user_avatar', 'rating',
                  'title', 'content', 'is_verified_purchase', 'is_approved',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'is_verified_purchase', 'created_at', 'updated_at')


class ProductTagSerializer(serializers.ModelSerializer):
    """
    مسلسل بيانات علامات المنتج
    """

    class Meta:
        model = ProductTag
        fields = ('id', 'name', 'slug', 'created_at')
        read_only_fields = ('id', 'created_at')


class ProductSerializer(serializers.ModelSerializer):
    """
    مسلسل بيانات المنتجات
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    main_image_url = serializers.SerializerMethodField()
    in_stock = serializers.BooleanField(read_only=True)
    total_inventory = serializers.IntegerField(read_only=True)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    tags = ProductTagSerializer(many=True, read_only=True, source='tags.tag')

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'short_description', 'sku',
                  'condition', 'category', 'category_name', 'brand', 'brand_name',
                  'is_active', 'is_featured', 'is_digital', 'track_inventory',
                  'created_at', 'updated_at', 'variants', 'images', 'main_image_url',
                  'in_stock', 'total_inventory', 'min_price', 'max_price',
                  'average_rating', 'review_count', 'tags')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_main_image_url(self, obj):
        request = self.context.get('request')
        main_image = obj.main_image
        if main_image and request:
            return request.build_absolute_uri(main_image.url)
        return None


class ProductDetailSerializer(ProductSerializer):
    """
    مسلسل بيانات تفاصيل المنتج
    """
    reviews = ProductReviewSerializer(many=True, read_only=True)
    related_products = serializers.SerializerMethodField()

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ('reviews', 'related_products')

    def get_related_products(self, obj):
        # الحصول على منتجات ذات صلة (من نفس الفئة)
        related_products = Product.objects.filter(
            category=obj.category,
            is_active=True
        ).exclude(id=obj.id)[:4]
        return ProductSerializer(related_products, many=True, context=self.context).data


class ProductListSerializer(serializers.ModelSerializer):
    """
    مسلسل بيانات قائمة المنتجات
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    main_image_url = serializers.SerializerMethodField()
    in_stock = serializers.BooleanField(read_only=True)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'short_description', 'category_name', 'brand_name',
                  'is_featured', 'is_digital', 'created_at', 'main_image_url',
                  'in_stock', 'min_price', 'average_rating', 'review_count')
        read_only_fields = ('id', 'created_at')

    def get_main_image_url(self, obj):
        request = self.context.get('request')
        main_image = obj.main_image
        if main_image and request:
            return request.build_absolute_uri(main_image.url)
        return None


class ProductAttributeSerializer(serializers.ModelSerializer):
    """
    مسلسل بيانات خصائص المنتج
    """
    values = ProductAttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ('id', 'name', 'created_at', 'values')
        read_only_fields = ('id', 'created_at')


class ProductFilterSerializer(serializers.Serializer):
    """
    مسلسل بيانات فلاتر المنتجات
    """
    category = serializers.IntegerField(required=False)
    brand = serializers.IntegerField(required=False)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    condition = serializers.CharField(required=False)
    is_featured = serializers.BooleanField(required=False)
    in_stock = serializers.BooleanField(required=False)
    rating = serializers.IntegerField(required=False)
    tags = serializers.ListField(child=serializers.IntegerField(), required=False)
    search = serializers.CharField(required=False)
    sort_by = serializers.ChoiceField(
        choices=[
            ('created_at', 'الأحدث'),
            ('price', 'السعر: من الأقل إلى الأعلى'),
            ('-price', 'السعر: من الأعلى إلى الأقل'),
            ('name', 'الاسم: أ-ي'),
            ('-name', 'الاسم: ي-أ'),
            ('-average_rating', 'التقييم'),
            ('-review_count', 'عدد المراجعات'),
        ],
        required=False
    )
