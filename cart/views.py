from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CartItem
from products.models import Product
from orders.models import Order


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, "cart/cart.html", {
        "cart_items": cart_items,
        "total": total
    })


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    item.delete()

    return redirect("cart")


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":

        Order.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            address=request.POST.get("address"),
            phone=request.POST.get("phone"),
            payment_method=request.POST.get("payment_method"),
            total_price=total,
        )

        # Clear the cart after placing the order
        cart_items.delete()

        messages.success(request, "Order placed successfully!")

        return redirect("products")

    return render(request, "cart/checkout.html", {
        "cart_items": cart_items,
        "total": total
    })