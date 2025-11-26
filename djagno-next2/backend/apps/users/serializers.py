from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, UserProfile, UserAddress


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    مسلسل تسجيل المستخدم الجديد
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'phone')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "كلمات المرور غير متطابقة"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    مسلسل بيانات المستخدم
    """
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'birth_date',
                  'avatar', 'country', 'city', 'address', 'postal_code', 'is_verified',
                  'date_joined', 'profile')
        read_only_fields = ('id', 'is_verified', 'date_joined')

    def get_profile(self, obj):
        try:
            profile = obj.profile
            return UserProfileSerializer(profile).data
        except UserProfile.DoesNotExist:
            return None


class UserProfileSerializer(serializers.ModelSerializer):
    """
    مسلسل بيانات ملف تعريف المستخدم
    """

    class Meta:
        model = UserProfile
        fields = ('bio', 'website', 'social_twitter', 'social_facebook', 'social_instagram',
                  'social_linkedin', 'newsletter_subscribed', 'sms_notifications',
                  'email_notifications', 'push_notifications')


class UserAddressSerializer(serializers.ModelSerializer):
    """
    مسلسل بيانات عناوين المستخدم
    """

    class Meta:
        model = UserAddress
        fields = ('id', 'address_type', 'title', 'address', 'city', 'postal_code',
                  'country', 'is_default', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class LoginSerializer(serializers.Serializer):
    """
    مسلسل تسجيل الدخول
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                              username=email, password=password)

            if not user:
                msg = 'البريد الإلكتروني أو كلمة المرور غير صحيحة'
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_active:
                msg = 'تم تعطيل حسابك'
                raise serializers.ValidationError(msg, code='authorization')

            attrs['user'] = user
            return attrs
        else:
            msg = 'يجب تضمين البريد الإلكتروني وكلمة المرور'
            raise serializers.ValidationError(msg, code='authorization')


class PasswordResetSerializer(serializers.Serializer):
    """
    مسلسل إعادة تعيين كلمة المرور
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('لا يوجد مستخدم مسجل بهذا البريد الإلكتروني')
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    مسلسل تأكيد إعادة تعيين كلمة المرور
    """
    token = serializers.CharField()
    uid = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "كلمات المرور غير متطابقة"})
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """
    مسلسل تغيير كلمة المرور
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('كلمة المرور الحالية غير صحيحة')
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "كلمات المرور غير متطابقة"})
        return attrs
