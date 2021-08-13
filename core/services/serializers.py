from django.contrib.auth import models
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Category, Comment, Order,  Message, Profile, RoleChoices, SubCategory
from core.handlers import create_user, fill_user_profile


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    subcategorys = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'subcategorys']


class ProfileCreateSerializer(serializers.ModelSerializer):
    role = serializers.MultipleChoiceField(choices=RoleChoices)
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['role', 'category']


user = {
    'user': {
        'username': 'boom',
        'email': 'baam',
        'profile': {
            'region': 'Yorsheer',
            'city': 'London',
            'role': ['client', 'worker'],
            'category': [
                {
                    'name': 'wow',
                    'subcategory': [
                        {'name': 'peeew'},
                    ]
                },
                {
                    'name': 'Crew',
                    'subcategory': [
                        {'name': 'sub'},
                        {'name': 'lub'},
                    ]
                },
            ]
        }
    }  
}


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False, validators=[
        UniqueValidator(queryset=User.objects.all())])
    profile = ProfileCreateSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'profile']

    def create(self, validated_data):
        user = create_user(validated_data)
        profile_data = validated_data.pop('profile')
        fill_user_profile(profile_data, user)

        category_data = validated_data.pop('category')
        cat_serializer = CategorySerializer(category_data)
        if cat_serializer.is_valid():
            pass

        return user


class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.MultipleChoiceField(choices=RoleChoices)
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['role', 'phone_number', 'description', 'work_experience',
         'category', 'region', 'city', 'is_juridical']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False, validators=[
        UniqueValidator(queryset=User.objects.all())])
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    work_experience = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(max_length=255, required=False)
    region = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=255, required=False)
    role = serializers.MultipleChoiceField(choices=RoleChoices, required=False)
    category = CategorySerializer(many=True, read_only=True)
    is_juridical = serializers.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = ['role', 'phone_number', 'description', 'work_experience',
         'category', 'region', 'city', 'is_juridical']


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
    order_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False)

    class Meta:
        depth = 1
        model = Order
        fields = ['id', 'uuid', 'user', 'title',
                  'slug', 'description', 'order_date', 'category', 'open']


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
