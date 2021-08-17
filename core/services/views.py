import status
from django.shortcuts import render
from django.http import Http404

from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_multiple_model.views import ObjectMultipleModelAPIView

from .models import Order
from .serializers import (
    CommentSerializer,
    OrderSerializer,
    MessageSerializer,
    UserSerializer,
    UserUpdateSerializer,
)


class OrderListView(ObjectMultipleModelAPIView):
    # permission_classes = [IsAuthenticated]

    def get_querylist(self):
        querylist = [
            {'queryset': User.objects.filter(username=self.request.user.username), 'serializer_class': UserSerializer},
            {'queryset': Order.objects.all(), 'serializer_class': OrderSerializer},
        ]

        return querylist


class OrderView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class UserDataUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        try:
            return User.objects.get(pk=request.user.pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request):
        user = self.get_object(request)
        serializer = UserUpdateSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
