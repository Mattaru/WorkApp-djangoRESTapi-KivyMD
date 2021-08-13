from django.urls import path

from .views import OrderListView, OrderView, UserDataUpdate


app_name = 'services'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>', OrderView.as_view(), name='order_detail'),
    path('user-update/', UserDataUpdate.as_view(), name='user_update'),
]
