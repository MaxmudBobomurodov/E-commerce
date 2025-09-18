from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from products.models import Product
from shared.utils.custom_response import CustomResponse


class OrderAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return CustomResponse.success(message_key="SUCCESS", data=serializer.data, request=request)


    def post(self, request):

        cart = Cart.objects.get(user=request.user)
        order = Order.objects.create(user=request.user, total_sum=0, status=False)
        product = Product.objects.all()

        total = 0
        total_quantity = 0
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            total += item.product.price * item.quantity

            item.product.quantity -= item.quantity
            item.product.save()

        order.total_sum = total

        product.quantity = total_quantity
        order.save()

        cart.items.all().delete()

        serializer = OrderSerializer(order)
        return CustomResponse.success(message_key="SUCCESS", data=serializer.data, request=request)

class AdminOrderListView(ListAPIView):
    queryset = Order.objects.all().select_related("user").prefetch_related("items")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        orders = self.get_queryset()
        serializer = self.serializer_class(orders, many=True)
        return CustomResponse.success(
            message_key="SUCCESS",
            data=serializer.data,
            request=request
        )
