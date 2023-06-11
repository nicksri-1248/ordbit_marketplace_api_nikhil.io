from django.db import models
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

#ORDER

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    quantity = models.PositiveIntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=10)
    address = models.CharField(max_length=200, default='')
    delivery_date = models.DateField(default=datetime.now)
    delivery_time = models.TimeField(default=timezone.now)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

#ORDER
