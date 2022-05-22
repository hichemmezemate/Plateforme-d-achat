import json

from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from app.forms import ProductForm
from app.models import Product, Cart, Item


# Create your views here.
class InventoryView(View):

    def get(self, request):
        products = Product.objects.all()
        return render(request, "inventory.html", {
            "products": products
        })


class ProductView(View):

    form_class = ProductForm

    def get(self, request):
        return render(request, "create-product.html")

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            product = Product()
            product.name = form.data['name']
            product.vat = float(form.data['vat'])
            product.price_ht = float(form.data['price_ht'])
            product.max_inventory = int(form.data['max_inventory'])
            product.ordered_inventory = int(form.data['ordered_inventory'])
            product.save()

        return redirect("inventory")


class CatalogView(View):

    def get(self, request):
        products = Product.objects.all()

        if "cart_id" in request.COOKIES and request.COOKIES["cart_id"] != 'None':
            cart = Cart.objects.filter(id=request.COOKIES["cart_id"]).first()
            if cart.checked_out:
                cart = None

        if cart is None:
            cart = Cart()
            cart.checked_out = False
            cart.save()

        response = render(request, "catalog.html", {
            "products": products,
            "cart": cart
        })

        response.set_cookie("cart_id", cart.id)

        return response

    def patch(self, request):
        if "cart_id" in request.COOKIES and request.COOKIES["cart_id"] != 'None':
            cart = Cart.objects.filter(id=request.COOKIES["cart_id"]).first()
            if cart.checked_out:
                cart = None

        if cart is None:
            return HttpResponse(status=404)

        body = json.loads(request.body)

        product_id = body["product_id"]
        quantity = body["quantity"]

        item = cart.items().filter(product_id=product_id).first()

        if item is not None:
            if quantity == 0:
                item.delete()
            else:
                item.quantity = quantity
                item.save()
        else:
            item = Item()
            item.cart_id = cart.id
            item.product_id = product_id
            item.quantity = quantity
            item.save()

        return HttpResponse(status=202)