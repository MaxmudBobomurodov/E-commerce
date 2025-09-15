from django.urls import path

from cart.views import CartItemAPIView

app_name = "orders"

urlpatterns = [
    path('',CartItemAPIView.as_view(), name='cart'),
    path('items/<int:pk>/',CartItemAPIView.as_view(), name='cart-item'),
]