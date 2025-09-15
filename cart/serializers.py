from rest_framework import serializers

from cart.models import Cart, CartItem
from products.models import Product
from shared.exceptions.custom_exceptions import CustomException


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    user = serializers.CharField(source="cart.user.username", read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_name", "quantity", "user"]
        extra_kwargs = {
            "cart": {"read_only": True}
        }

    def validate(self, data):
        product = data.get("product")
        requested_quantity = data.get("quantity")

        if product.quantity < requested_quantity:
            raise CustomException(
                message_key="BAD_REQUEST",
            )
        return data


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "items"]
