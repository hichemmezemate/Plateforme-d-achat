from django import forms
from django.core.exceptions import ValidationError


class ProductForm(forms.Form):
    name = forms.CharField(max_length=64)
    price_ht = forms.FloatField()
    vat = forms.FloatField()
    ordered_inventory = forms.IntegerField()
    max_inventory = forms.IntegerField()

    def clean(self):
        cd = self.cleaned_data
        vat = cd.get('vat')
        if vat == 0.055 or vat == 0.2:
            return cd
        raise ValidationError("wrong vat value")
