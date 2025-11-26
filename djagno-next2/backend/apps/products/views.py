from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db import models
from django.db.models import Avg, Count
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as drf_filters
from .models import (
    Category, Brand, Product, ProductVariant, ProductAttribute,
    ProductAttributeValue, ProductVariantAttribute, ProductImage,
    ProductReview, ProductTag, ProductTagRelation
)
from .serializers import (
    CategorySerializer, BrandSerializer, ProductSerializer, ProductDetailSerializer,
    ProductListSerializer, ProductVariantSerializer, ProductAttributeSerializer,
    ProductAttributeValueSerializer, ProductImageSerializer, ProductReviewSerializer,
    ProductTagSerializer, ProductFilterSerializer
)
from apps.users.permissions import IsAdminOrOwner


class ProductFilter(drf_filters.FilterSet):
    """
    فلاتر المنتجات
    """
    min_price = drf_filters.NumberFilter(field_name="variants__price", lookup_expr='gte')
    max_price = drf_filters.NumberFilter(field_name="variants__price", lookup_expr='lte')
    category = drf_filters.NumberFilter(field_name="category__id")
    brand = drf_filters.NumberFilter(field_name="brand__id")
    condition = drf_filters.ChoiceFilter(choices=Product.CONDITION_CHOICES)
    in_stock = drf_filters.BooleanFilter(method='filter_in_stock')
    rating = drf_filters.NumberFilter(method='filter_rating')
    tags = drf_filters.ModelMultipleChoiceFilter(
        field_name='tags__tag',
        queryset=ProductTag.objects.all(),
        to_field_name='id'
    )

    class Meta:
        model = Product
        fields = ['is_featured', 'is_digital']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(variants__inventory__gt=0).distinct()
        return queryset

    def filter_rating(self, queryset, name, value):
        return queryset.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=value)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج الفئات
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """
        الحصول على منتجات فئة معينة
        """
        category = self.get_object()
        products = Product.objects.filter(
            category__in=category.get_descendants(include_self=True),
            is_active=True
        ).distinct()
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class BrandViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج العلامات التجارية
    """
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'country_of_origin']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """
        الحصول على منتجات علامة تجارية معينة
        """
        brand = self.get_object()
        products = Product.objects.filter(brand=brand, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج المنتجات
    """
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'short_description', 'sku']
    ordering_fields = ['name', 'created_at', 'price']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_review(self, request, pk=None):
        """
        إضافة مراجعة للمنتج
        """
        product = self.get_object()
        
        # التحقق من أن المستخدم لم يقم بمراجعة المنتج من قبل
        if ProductReview.objects.filter(product=product, user=request.user).exists():
            return Response(
                {'error': _('لقد قمت بمراجعة هذا المنتج من قبل')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # إنشاء مراجعة جديدة
        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        """
        الحصول على منتجات مشابهة
        """
        product = self.get_object()
        
        # الحصول على منتجات من نفس الفئة
        similar_products = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:4]
        
        serializer = ProductListSerializer(similar_products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductVariantViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج متغيرات المنتج
    """
    queryset = ProductVariant.objects.filter(is_active=True)
    serializer_class = ProductVariantSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'is_active']
    search_fields = ['name', 'sku']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductAttributeViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج خصائص المنتج
    """
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductAttributeValueViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج قيم خصائص المنتج
    """
    queryset = ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['attribute']
    search_fields = ['value']
    ordering_fields = ['value', 'created_at']
    ordering = ['value']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductImageViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج صور المنتج
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'is_main']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductReviewViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج مراجعات المنتج
    """
    queryset = ProductReview.objects.filter(is_approved=True)
    serializer_class = ProductReviewSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'user', 'rating', 'is_verified_purchase']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        # التحقق من أن المستخدم لم يقم بمراجعة المنتج من قبل
        product = serializer.validated_data['product']
        if ProductReview.objects.filter(product=product, user=self.request.user).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError(_('لقد قمت بمراجعة هذا المنتج من قبل'))
        
        serializer.save(user=self.request.user)


class ProductTagViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج علامات المنتج
    """
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """
        الحصول على منتجات بعلامة معينة
        """
        tag = self.get_object()
        products = Product.objects.filter(tags__tag=tag, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class FeaturedProductsView(APIView):
    """
    عرض للمنتجات المميزة
    """
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.filter(is_featured=True, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?page={page_obj.next_page_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?page={page_obj.previous_page_number()}'),
            'results': serializer.data
        })


class ProductSearchView(APIView):
    """
    عرض للبحث عن المنتجات
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('q', '')
        if not query:
            return Response({'error': _('يجب إدخال كلمة بحث')}, status=status.HTTP_400_BAD_REQUEST)
        
        products = Product.objects.filter(
            is_active=True
        ).filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(short_description__icontains=query) |
            models.Q(sku__icontains=query) |
            models.Q(brand__name__icontains=query) |
            models.Q(category__name__icontains=query) |
            models.Q(tags__tag__name__icontains=query)
        ).distinct()
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'query': query,
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?q={query}&page={page_obj.next_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?q={query}&page={page_obj.previous_number()}'),
            'results': serializer.data
        })


class ProductFiltersView(APIView):
    """
    عرض للحصول على خيارات الفلترة المتاحة
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # الحصول على الفئات
        categories = Category.objects.filter(is_active=True)
        categories_data = CategorySerializer(categories, many=True).data
        
        # الحصول على العلامات التجارية
        brands = Brand.objects.filter(is_active=True)
        brands_data = BrandSerializer(brands, many=True).data
        
        # الحصول على العلامات
        tags = ProductTag.objects.all()
        tags_data = ProductTagSerializer(tags, many=True).data
        
        # الحصول على نطاق الأسعار
        price_range = ProductVariant.objects.aggregate(
            min_price=models.Min('price'),
            max_price=models.Max('price')
        )
        
        return Response({
            'categories': categories_data,
            'brands': brands_data,
            'tags': tags_data,
            'price_range': price_range,
            'conditions': Product.CONDITION_CHOICES,
            'sort_options': [
                {'value': 'created_at', 'label': _('الأحدث')},
                {'value': 'price', 'label': _('السعر: من الأقل إلى الأعلى')},
                {'value': '-price', 'label': _('السعر: من الأعلى إلى الأقل')},
                {'value': 'name', 'label': _('الاسم: أ-ي')},
                {'value': '-name', 'label': _('الاسم: ي-أ')},
                {'value': '-average_rating', 'label': _('التقييم')},
                {'value': '-review_count', 'label': _('عدد المراجعات')},
            ]
        })


class CategoryProductsView(APIView):
    """
    عرض للمنتجات حسب الفئة
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug, is_active=True)
        products = Product.objects.filter(
            category__in=category.get_descendants(include_self=True),
            is_active=True
        ).distinct()
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'category': CategorySerializer(category).data,
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?page={page_obj.next_page_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?page={page_obj.previous_page_number()}'),
            'results': serializer.data
        })


class BrandProductsView(APIView):
    """
    عرض للمنتجات حسب العلامة التجارية
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        brand = get_object_or_404(Brand, slug=slug, is_active=True)
        products = Product.objects.filter(brand=brand, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'brand': BrandSerializer(brand).data,
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?page={page_obj.next_page_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?page={page_obj.previous_page_number()}'),
            'results': serializer.data
        })


class TagProductsView(APIView):
    """
    عرض للمنتجات حسب العلامة
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        tag = get_object_or_404(ProductTag, slug=slug)
        products = Product.objects.filter(tags__tag=tag, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'tag': ProductTagSerializer(tag).data,
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?page={page_obj.next_page_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?page={page_obj.previous_page_number()}'),
            'results': serializer.data
        })


class SimilarProductsView(APIView):
    """
    عرض للمنتجات المشابهة
    """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_active=True)
        
        # الحصول على منتجات من نفس الفئة
        similar_products = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:8]
        
        serializer = ProductListSerializer(similar_products, many=True, context={'request': request})
        return Response(serializer.data)
    
    queryset = ProductVariant.objects.filter(is_active=True)
    serializer_class = ProductVariantSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'is_active']
    search_fields = ['name', 'sku']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductAttributeViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج خصائص المنتج
    """
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductAttributeValueViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج قيم خصائص المنتج
    """
    queryset = ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['attribute']
    search_fields = ['value']
    ordering_fields = ['value', 'created_at']
    ordering = ['value']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductImageViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج صور المنتج
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'is_main']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductReviewViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج مراجعات المنتج
    """
    queryset = ProductReview.objects.filter(is_approved=True)
    serializer_class = ProductReviewSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'user', 'rating', 'is_verified_purchase']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        # التحقق من أن المستخدم لم يقم بمراجعة المنتج من قبل
        product = serializer.validated_data['product']
        if ProductReview.objects.filter(product=product, user=self.request.user).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError(_('لقد قمت بمراجعة هذا المنتج من قبل'))
        
        serializer.save(user=self.request.user)


class ProductTagViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج علامات المنتج
    """
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """
        الحصول على منتجات بعلامة معينة
        """
        tag = self.get_object()
        products = Product.objects.filter(tags__tag=tag, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class FeaturedProductsView(APIView):
    """
    عرض للمنتجات المميزة
    """
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.filter(is_featured=True, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?page={page_obj.next_page_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?page={page_obj.previous_page_number()}'),
            'results': serializer.data
        })


class ProductSearchView(APIView):
    """
    عرض للبحث عن المنتجات
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('q', '')
        if not query:
            return Response({'error': _('يجب إدخال كلمة بحث')}, status=status.HTTP_400_BAD_REQUEST)
        
        products = Product.objects.filter(
            is_active=True
        ).filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(short_description__icontains=query) |
            models.Q(sku__icontains=query) |
            models.Q(brand__name__icontains=query) |
            models.Q(category__name__icontains=query) |
            models.Q(tags__tag__name__icontains=query)
        ).distinct()
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'query': query,
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?q={query}&page={page_obj.next_page_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?q={query}&page={page_obj.previous_page_number()}'),
            'results': serializer.data
        })


class ProductFiltersView(APIView):
    """
    عرض للحصول على خيارات الفلترة المتاحة
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # الحصول على الفئات
        categories = Category.objects.filter(is_active=True)
        categories_data = CategorySerializer(categories, many=True).data
        
        # الحصول على العلامات التجارية
        brands = Brand.objects.filter(is_active=True)
        brands_data = BrandSerializer(brands, many=True).data
        
        # الحصول على العلامات
        tags = ProductTag.objects.all()
        tags_data = ProductTagSerializer(tags, many=True).data
        
        # الحصول على نطاق الأسعار
        price_range = ProductVariant.objects.aggregate(
            min_price=models.Min('price'),
            max_price=models.Max('price')
        )
        
        return Response({
            'categories': categories_data,
            'brands': brands_data,
            'tags': tags_data,
            'price_range': price_range,
            'conditions': Product.CONDITION_CHOICES,
            'sort_options': [
                {'value': 'created_at', 'label': _('الأحدث')},
                {'value': 'price', 'label': _('السعر: من الأقل إلى الأعلى')},
                {'value': '-price', 'label': _('السعر: من الأعلى إلى الأقل')},
                {'value': 'name', 'label': _('الاسم: أ-ي')},
                {'value': '-name', 'label': _('الاسم: ي-أ')},
                {'value': '-average_rating', 'label': _('التقييم')},
                {'value': '-review_count', 'label': _('عدد المراجعات')},
            ]
        })


class CategoryProductsView(APIView):
    """
    عرض للمنتجات حسب الفئة
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug, is_active=True)
        products = Product.objects.filter(
            category__in=category.get_descendants(include_self=True),
            is_active=True
        ).distinct()
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'category': CategorySerializer(category).data,
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?page={page_obj.next_page_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?page={page_obj.previous_page_number()}'),
            'results': serializer.data
        })


class BrandProductsView(APIView):
    """
    عرض للمنتجات حسب العلامة التجارية
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        brand = get_object_or_404(Brand, slug=slug, is_active=True)
        products = Product.objects.filter(brand=brand, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'brand': BrandSerializer(brand).data,
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?page={page_obj.next_page_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?page={page_obj.previous_page_number()}'),
            'results': serializer.data
        })


class TagProductsView(APIView):
    """
    عرض للمنتجات حسب العلامة
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        tag = get_object_or_404(ProductTag, slug=slug)
        products = Product.objects.filter(tags__tag=tag, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'tag': ProductTagSerializer(tag).data,
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?page={page_obj.next_page_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?page={page_obj.previous_page_number()}'),
            'results': serializer.data
        })


class SimilarProductsView(APIView):
    """
    عرض للمنتجات المشابهة
    """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_active=True)
        
        # الحصول على منتجات من نفس الفئة
        similar_products = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:8]
        
        serializer = ProductListSerializer(similar_products, many=True, context={'request': request})
        return Response(serializer.data)
    
    queryset = ProductVariant.objects.filter(is_active=True)
    serializer_class = ProductVariantSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'is_active']
    search_fields = ['name', 'sku']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductAttributeViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج خصائص المنتج
    """
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductAttributeValueViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج قيم خصائص المنتج
    """
    queryset = ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['attribute']
    search_fields = ['value']
    ordering_fields = ['value', 'created_at']
    ordering = ['value']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductImageViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج صور المنتج
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'is_main']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductReviewViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج مراجعات المنتج
    """
    queryset = ProductReview.objects.filter(is_approved=True)
    serializer_class = ProductReviewSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'user', 'rating', 'is_verified_purchase']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        # التحقق من أن المستخدم لم يقم بمراجعة المنتج من قبل
        product = serializer.validated_data['product']
        if ProductReview.objects.filter(product=product, user=self.request.user).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError(_('لقد قمت بمراجعة هذا المنتج من قبل'))
        
        serializer.save(user=self.request.user)


class ProductTagViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج علامات المنتج
    """
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """
        الحصول على منتجات بعلامة معينة
        """
        tag = self.get_object()
        products = Product.objects.filter(tags__tag=tag, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class FeaturedProductsView(APIView):
    """
    عرض للمنتجات المميزة
    """
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.filter(is_featured=True, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?page={page_obj.next_page_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?page={page_obj.previous_page_number()}'),
            'results': serializer.data
        })


class ProductSearchView(APIView):
    """
    عرض للبحث عن المنتجات
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('q', '')
        if not query:
            return Response({'error': _('يجب إدخال كلمة بحث')}, status=status.HTTP_400_BAD_REQUEST)
        
        products = Product.objects.filter(
            is_active=True
        ).filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(short_description__icontains=query) |
            models.Q(sku__icontains=query) |
            models.Q(brand__name__icontains=query) |
            models.Q(category__name__icontains=query) |
            models.Q(tags__tag__name__icontains=query)
        ).distinct()
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'query': query,
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?q={query}&page={page_obj.next_page_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?q={query}&page={page_obj.previous_page_number()}'),
            'results': serializer.data
        })


class ProductFiltersView(APIView):
    """
    عرض للحصول على خيارات الفلترة المتاحة
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # الحصول على الفئات
        categories = Category.objects.filter(is_active=True)
        categories_data = CategorySerializer(categories, many=True).data
        
        # الحصول على العلامات التجارية
        brands = Brand.objects.filter(is_active=True)
        brands_data = BrandSerializer(brands, many=True).data
        
        # الحصول على العلامات
        tags = ProductTag.objects.all()
        tags_data = ProductTagSerializer(tags, many=True).data
        
        # الحصول على نطاق الأسعار
        price_range = ProductVariant.objects.aggregate(
            min_price=models.Min('price'),
            max_price=models.Max('price')
        )
        
        return Response({
            'categories': categories_data,
            'brands': brands_data,
            'tags': tags_data,
            'price_range': price_range,
            'conditions': Product.CONDITION_CHOICES,
            'sort_options': [
                {'value': 'created_at', 'label': _('الأحدث')},
                {'value': 'price', 'label': _('السعر: من الأقل إلى الأعلى')},
                {'value': '-price', 'label': _('السعر: من الأعلى إلى الأقل')},
                {'value': 'name', 'label': _('الاسم: أ-ي')},
                {'value': '-name', 'label': _('الاسم: ي-أ')},
                {'value': '-average_rating', 'label': _('التقييم')},
                {'value': '-review_count', 'label': _('عدد المراجعات')},
            ]
        })


class CategoryProductsView(APIView):
    """
    عرض للمنتجات حسب الفئة
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug, is_active=True)
        products = Product.objects.filter(
            category__in=category.get_descendants(include_self=True),
            is_active=True
        ).distinct()
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'category': CategorySerializer(category).data,
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?page={page_obj.next_page_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?page={page_obj.previous_page_number()}'),
            'results': serializer.data
        })


class BrandProductsView(APIView):
    """
    عرض للمنتجات حسب العلامة التجارية
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        brand = get_object_or_404(Brand, slug=slug, is_active=True)
        products = Product.objects.filter(brand=brand, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'brand': BrandSerializer(brand).data,
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?page={page_obj.next_page_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?page={page_obj.previous_page_number()}'),
            'results': serializer.data
        })


class TagProductsView(APIView):
    """
    عرض للمنتجات حسب العلامة
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        tag = get_object_or_404(ProductTag, slug=slug)
        products = Product.objects.filter(tags__tag=tag, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page_size = int(request.GET.get('page_size', 12))
        from django.core.paginator import Paginator
        paginator = Paginator(products, page_size)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ProductListSerializer(page_obj, many=True, context={'request': request})
        return Response({
            'tag': ProductTagSerializer(tag).data,
            'count': paginator.count,
            'next': page_obj.has_next() and request.build_absolute_uri(f'?page={page_obj.next_page_number()}'),
            'previous': page_obj.has_previous() and request.build_absolute_uri(f'?page={page_obj.previous_page_number()}'),
            'results': serializer.data
        })


class SimilarProductsView(APIView):
    """
    عرض للمنتجات المشابهة
    """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_active=True)
        
        # الحصول على منتجات من نفس الفئة
        similar_products = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:8]
        
        serializer = ProductListSerializer(similar_products, many=True, context={'request': request})
        return Response(serializer.data)مات المنتج

    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """
        الحصول على منتجات بعلامة معينة
        """
        tag = self.get_object()
        products = Product.objects.filter(tags__tag=tag, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class FeaturedProductsView(APIView):
    """
    عرض للمنتجات المميزة
    """
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.filter(is_featured=True, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترقيم الصفحات
        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(products, request)
        
        serializer = ProductListSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class ProductSearchView(APIView):
    """
    عرض للبحث عن المنتجات
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('q', '')
        if not query:
            return Response({'error': _('يجب إدخال كلمة بحث')}, status=status.HTTP_400_BAD_REQUEST)
        
        products = Product.objects.filter(
            is_active=True
        ).filter(
            name__icontains=query
        ).filter(
            description__icontains=query
        ).distinct()
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(products, request)
        
        serializer = ProductListSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class ProductFiltersView(APIView):
    """
    عرض للحصول على خيارات الفلترة المتاحة للمنتجات
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # الحصول على الفئات
        categories = Category.objects.filter(is_active=True)
        category_data = CategorySerializer(categories, many=True).data
        
        # الحصول على العلامات التجارية
        brands = Brand.objects.filter(is_active=True)
        brand_data = BrandSerializer(brands, many=True).data
        
        # الحصول على العلامات
        tags = ProductTag.objects.all()
        tag_data = ProductTagSerializer(tags, many=True).data
        
        # الحصول على نطاق الأسعار
        price_range = ProductVariant.objects.aggregate(
            min_price=models.Min('price'),
            max_price=models.Max('price')
        )
        
        return Response({
            'categories': category_data,
            'brands': brand_data,
            'tags': tag_data,
            'price_range': price_range,
            'conditions': [{'value': choice[0], 'label': choice[1]} for choice in Product.CONDITION_CHOICES]
        })


class CategoryProductsView(APIView):
    """
    عرض للمنتجات حسب الفئة
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug, is_active=True)
        products = Product.objects.filter(
            category__in=category.get_descendants(include_self=True),
            is_active=True
        ).distinct()
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(products, request)
        
        serializer = ProductListSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class BrandProductsView(APIView):
    """
    عرض للمنتجات حسب العلامة التجارية
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        brand = get_object_or_404(Brand, slug=slug, is_active=True)
        products = Product.objects.filter(brand=brand, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(products, request)
        
        serializer = ProductListSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class TagProductsView(APIView):
    """
    عرض للمنتجات حسب العلامة
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        tag = get_object_or_404(ProductTag, slug=slug)
        products = Product.objects.filter(tags__tag=tag, is_active=True)
        
        # تطبيق الفلاتر
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        # ترتيب النتائج
        sort_by = request.GET.get('sort_by', '-created_at')
        products = products.order_by(sort_by)
        
        # ترقيم الصفحات
        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(products, request)
        
        serializer = ProductListSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class SimilarProductsView(APIView):
    """
    عرض للمنتجات المشابهة
    """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_active=True)
        
        # الحصول على منتجات من نفس الفئة
        similar_products = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:8]
        
        serializer = ProductListSerializer(similar_products, many=True, context={'request': request})
        return Response(serializer.data)
