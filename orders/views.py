from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Order
from cart.models import CartItem


@login_required
def orders(request):
    order_list = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "orders/orders.html", {
        "orders": order_list
    })


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "total": total
    })


@login_required
def place_order(request):

    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect("cart")

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    Order.objects.create(
        user=request.user,
        full_name=request.user.username,
        address="Demo Address",
        phone="9999999999",
        payment_method="COD",
        total_price=total
    )

    cart_items.delete()

    return redirect("orders")