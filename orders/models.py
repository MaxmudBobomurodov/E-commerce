from django.contrib.auth.models import User
from django.db import models

from products.models import BaseModel, Product


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)