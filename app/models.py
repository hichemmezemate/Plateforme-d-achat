from django.db import models


# Create your models here.
from django.template.defaultfilters import register


class Product(models.Model):
    name = models.CharField(blank=False, max_length=64)
    price_ht = models.FloatField(blank=False, null=False)
    vat = models.FloatField(blank=False, null=False)
    ordered_inventory = models.IntegerField(blank=False, null=False, default=0)
    max_inventory = models.IntegerField(blank=False, null=False)

    def price_ttc(self):
        return self.price_ht * self.vat + self.price_ht

    def available_inventory(self):
        return self.max_inventory - self.ordered_inventory


class Cart(models.Model):
    checked_out = models.BooleanField(default=False)

    def items(self):
        return Item.objects.filter(cart_id=self.id)

    def total_ttc(self):
        total_ttc = 0
        for item in self.items():
            total_ttc = total_ttc + item.product.price_ttc() * item.quantity
        return total_ttc


class Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def total_ttc(self):
        return self.product.price_ttc() * self.quantity
