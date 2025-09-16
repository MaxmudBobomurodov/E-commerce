from django.urls import path

from orders.views import OrderAPIView

app_name = 'orders'

urlpatterns = [
    path("",OrderAPIView.as_view(), name='order-list'),
]