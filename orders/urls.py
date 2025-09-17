from django.urls import path

from orders.views import OrderAPIView, AdminOrderListView

app_name = 'orders'

urlpatterns = [
    path("",OrderAPIView.as_view(), name='order-list'),
    path("admin/",AdminOrderListView.as_view()),
]