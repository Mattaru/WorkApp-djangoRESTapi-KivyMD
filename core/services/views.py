import status
from django.shortcuts import render

from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers import (
    CommentSerializer,
    OrderSerializer,
    MessageSerializer,
    UserSerializer,
    ProfileSerializer
)


class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class OrderView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
