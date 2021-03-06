from django.contrib.auth import models
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Category, Comment, Order, Firm,  Message, Profile, RoleChoices, SubCategory
from core.handlers import create_user, fill_user_profile


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name']


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = SubCategory
        fields = ['name', 'category']


class SubCategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ['name']


class CategoryCreateSerializer(serializers.ModelSerializer):
    subcategories = SubCategoryCreateSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Category
        fields = ['name', 'subcategories']


class CategoryListSerializer(serializers.ModelSerializer):
    subcategories = SubCategoryCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'subcategories']


class FirmCreateSerializer(serializers.ModelSerializer):
    categories = CategoryCreateSerializer(many=True, read_only=False, required=False)
    subcategories = SubCategoryCreateSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Firm
        fields = ['name', 'categories', 'subcategories']


class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.MultipleChoiceField(choices=RoleChoices)
    categories = CategorySerializer(many=True, read_only=True)
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['avatar', 'role', 'phone_number', 'description', 'work_experience',
         'categories', 'subcategories', 'region', 'city', 'is_juridical']


class ProfileCreateSerializer(serializers.ModelSerializer):
    role = serializers.MultipleChoiceField(choices=RoleChoices)
    firm = FirmCreateSerializer(many=False, read_only=False, required=False)
    categories = CategoryCreateSerializer(many=True, read_only=False, required=False)
    subcategories = SubCategoryCreateSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Profile
        fields = ['role', 'firm', 'categories', 'subcategories']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None, allow_empty_file=False, required=False)
    description = serializers.CharField(required=False)
    work_experience = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(max_length=255, required=False)
    region = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=255, required=False)
    role = serializers.MultipleChoiceField(choices=RoleChoices, required=False)
    categories = CategorySerializer(many=True, read_only=True, required=False)
    subcategories = SubCategorySerializer(many=True, read_only=True, required=False)
    is_juridical = serializers.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'role', 'phone_number', 'description', 'work_experience',
         'categories', 'subcategories', 'region', 'city', 'is_juridical']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False, validators=[
        UniqueValidator(queryset=User.objects.all())])
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile']


class UserCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(allow_blank=False, validators=[
        UniqueValidator(queryset=User.objects.all())])
    profile = ProfileCreateSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'profile']

    def create(self, validated_data):
        
        user = create_user(validated_data)
        profile_data = validated_data.pop('profile')
        fill_user_profile(profile_data, user)
        category_data = profile_data.pop('categories')
        subcategory_data = profile_data.pop('subcategories')
        firm_data = profile_data.pop('firm')
        
        if firm_data:
            try:
                firm = Firm.objects.get(name=firm_data['name'])
            except Firm.DoesNotExist: 
                firm = Firm.objects.create(name=firm_data['name'])

            user.profile.firm = firm
            user.profile.save()
        
        if category_data:
            for cat in category_data:
                try:
                    category = Category.objects.get(name=cat['name'])
                except Category.DoesNotExist:
                    category = Category.objects.create(name=cat['name'])

                if firm_data:
                    user.profile.firm.categories.add(category)   
                else:
                    user.profile.categories.add(category)

        if subcategory_data:
            for subcat in subcategory_data:
                try:
                    subcategory = SubCategory.objects.get(name=subcat['name'])
                except SubCategory.DoesNotExist:
                    subcategory = SubCategory.objects.create(category=category, name=subcat['name'])
                
                if firm_data:
                    user.profile.firm.subcategories.add(subcategory)
                else:
                    user.profile.subcategories.add(subcategory)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(allow_blank=False, validators=[
        UniqueValidator(queryset=User.objects.all())], required=False)
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile']
   
    def update(self, instance, validated_data):
        if validated_data.get('profile'):
            profile_data = validated_data.get('profile')
            profile_serializer = ProfileUpdateSerializer(data=profile_data)

            if profile_serializer.is_valid():
                profile = profile_serializer.update(
                    instance.profile,
                    profile_serializer.validated_data
                )
                validated_data['profile'] = profile

        return super().update(instance, validated_data)


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    category = CategorySerializer()
    subcategory = SubCategorySerializer()
    order_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False)

    class Meta:
        depth = 1
        model = Order
        fields = ['user', 'uuid',  'title',
                  'slug', 'description', 'order_date', 'category', 'subcategory', 'open']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    order = OrderSerializer(required=False)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'order', 'timestamp', 'text']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(required=False)
    receiver = UserSerializer(required=False)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'timestamp', 'text', 'is_read']
