from requests import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from cart.models import CartItem, Cart
from cart.serializers import CartItemSerializer
from products.models import Product
from shared.utils.custom_response import CustomResponse


class CartItemAPIView(APIView):
    serializer_class = CartItemSerializer

    def get_permissions(self):
        if self.request.method=='GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        cart_items = CartItem.objects.filter(cart__user=request.user.id)
        serializer = CartItemSerializer(cart_items, many=True)
        return CustomResponse.success(message_key="SUCCESS", data=serializer.data,request=request)

    def post(self, request):
        data = request.data.copy()

        # userning savatini olish yoki yaratish
        cart, created = Cart.objects.get_or_create(user=request.user)
        # serializer
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(cart=cart)  # shu yerda cart ni qo‘shamiz
            return CustomResponse.success(
                message_key="SUCCESS",
                data=serializer.data,
                request=request
            )

    def put(self, request, pk=None):
        instance = get_object_or_404(CartItem, pk=pk,cart__user=request.user.id)
        serializer = self.serializer_class(instance ,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse.success(message_key="SUCCESS", data=serializer.data,request=request)

    def patch(self, request, pk=None):
        instance = get_object_or_404(CartItem, pk=pk,cart__user=request.user.id)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse.success(message_key="SUCCESS", data=serializer.data,request=request)

    def delete(self, request, pk=None):
        instance = get_object_or_404(CartItem, pk=pk, cart__user=request.user.id)
        instance.delete()
        return CustomResponse.success(message_key="SUCCESS", data={"message":"deleted"},request=request)