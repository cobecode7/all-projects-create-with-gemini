from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import UserProfile, UserAddress
from .serializers import (
    UserRegistrationSerializer, UserSerializer, UserProfileSerializer,
    UserAddressSerializer, LoginSerializer, PasswordResetSerializer,
    PasswordResetConfirmSerializer, ChangePasswordSerializer
)

User = get_user_model()


class RegisterView(APIView):
    """
    عرض لتسجيل مستخدم جديد
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    عرض لتسجيل الدخول
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    عرض لتسجيل الخروج
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    """
    عرض لتحديث رمز JWT
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        refresh = request.data.get('refresh')
        if not refresh:
            return Response({'error': _'يجب توفير رمز التحديث'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh)
            return Response({'access': str(token.access_token)})
        except Exception:
            return Response({'error': _'رمز التحديث غير صالح أو منتهي الصلاحية'}, status=status.HTTP_401_UNAUTHORIZED)


class VerifyEmailView(APIView):
    """
    عرض للتحقق من البريد الإلكتروني
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        # هنا سنقوم بتنفيذ منطق التحقق من البريد الإلكتروني
        # سنحتاج إلى إرسال رمز تحقق عبر البريد الإلكتروني
        return Response({'message': _'تم إرسال رمز التحقق إلى بريدك الإلكتروني'})


class PasswordResetView(APIView):
    """
    عرض لإعادة تعيين كلمة المرور
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            # هنا سنقوم بتنفيذ منطق إرسال رابط إعادة تعيين كلمة المرور
            email = serializer.validated_data['email']
            return Response({'message': _'تم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """
    عرض لتأكيد إعادة تعيين كلمة المرور
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            # هنا سنقوم بتنفيذ منطق التحقق من الرمز وتحديث كلمة المرور
            return Response({'message': _'تم تحديث كلمة المرور بنجاح'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    عرض لتغيير كلمة المرور
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'message': _'تم تغيير كلمة المرور بنجاح'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج المستخدم
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # المستخدمون العاديون يمكنهم رؤية بياناتهم فقط
        if not self.request.user.is_staff:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()

    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        عرض وتحديث بيانات المستخدم الحالي
        """
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج ملف تعريف المستخدم
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # المستخدمون العاديون يمكنهم رؤية بياناتهم فقط
        if not self.request.user.is_staff:
            return UserProfile.objects.filter(user=self.request.user)
        return UserProfile.objects.all()

    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        عرض وتحديث بيانات ملف تعريف المستخدم الحالي
        """
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
            
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAddressViewSet(viewsets.ModelViewSet):
    """
    مجموعة المشاهدات لنموذج عناوين المستخدم
    """
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # المستخدمون العاديون يمكنهم رؤية بياناتهم فقط
        if not self.request.user.is_staff:
            return UserAddress.objects.filter(user=self.request.user)
        return UserAddress.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def set_default(self, request, pk=None):
        """
        تعيين عنوان كعنوان افتراضي
        """
        address = self.get_object()
        
        # إلغاء جميع العناوين الافتراضية الأخرى
        UserAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)
        
        # تعيين العنوان الحالي كافتراضي
        address.is_default = True
        address.save()
        
        return Response({'message': _'تم تعيين العنوان كعنوان افتراضي'})
