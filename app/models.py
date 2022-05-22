from django.db import models


# Create your models here.
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
