from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import CategoryChoices, Comment, Order,  Message, Profile, RoleChoices
from core.handlers import create_user, fill_user_profile


class ProfileCreateSerializer(serializers.ModelSerializer):
    role = serializers.MultipleChoiceField(choices=RoleChoices)
    category = serializers.MultipleChoiceField(choices=CategoryChoices)

    class Meta:
        model = Profile
        fields = ['role', 'category']


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

        return user


class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.MultipleChoiceField(choices=RoleChoices)
    category = serializers.MultipleChoiceField(choices=CategoryChoices)

    class Meta:
        model = Profile
        fields = ['role', 'category', 'region', 'city']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False, validators=[
        UniqueValidator(queryset=User.objects.all())])
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'profile']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    category = serializers.MultipleChoiceField(choices=CategoryChoices)

    class Meta:
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
