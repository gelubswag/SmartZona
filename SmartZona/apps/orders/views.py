from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Order, OrderItem
from .forms import OrderItemForm
from SmartZona.apps.users.decorators import allowed_roles
from SmartZona.apps.warehouse.models import Loader


@method_decorator(allowed_roles(['customer', 'driver']), 'dispatch')
class IndexView(View):
    def get(self, request):
        if request.user.role.name == 'customer':
            orders = Order.objects.filter(customer=request.user)
        else:
            orders = list(
                Order.objects.filter(status='processing').all()
                ) + list(
                    Order.objects.filter(driver=request.user).all()
                )
        return render(request, 'orders/index.html', {'objects': orders})

    def post(self, request):
        order = Order.objects.create(customer=request.user)
        return redirect('orders:detail', pk=order.id)

@method_decorator(allowed_roles(['customer', 'driver']), 'dispatch')
class OrderDetailView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return render(request, 'orders/detail.html', {
            'order': order,
            'items': order.items.all(),
            'item_form': OrderItemForm(),
            'loaders': Loader.objects.filter(is_available=True) if order.status == 'processing' else None
        })

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        action = request.POST.get('action')

        if request.user.role.name == 'customer':
            if order.status == 'created':
                if action == 'add_item':
                    form = OrderItemForm(request.POST)
                    if form.is_valid():
                        item = form.save(commit=False)
                        item.order = order
                        try:
                            item.full_clean()
                            item.save()
                            messages.success(request, "Товар добавлен")
                        except ValidationError as e:
                            messages.error(request, e.messages[0])

                elif action == 'update_item':
                    item_id = request.POST.get('item_id')
                    new_quantity = int(request.POST.get('quantity'))
                    item = get_object_or_404(OrderItem, id=item_id, order=order)
                    if new_quantity <= item.product.quantity:
                        item.quantity = new_quantity
                        item.save()
                        messages.success(request, "Количество обновлено")
                    else:
                        messages.error(request, "Недостаточно товара на складе")

                elif action == 'delete_item':
                    item_id = request.POST.get('item_id')
                    item = get_object_or_404(OrderItem, id=item_id, order=order)
                    item.delete()
                    messages.success(request, "Товар удален")

                elif action == 'submit_order':
                    try:
                        order.full_clean()
                        order.status = 'processing'
                        order.save()
                        messages.success(request, "Заказ отправлен на сборку")
                    except ValidationError as e:
                        messages.error(request, e.messages[0])

        elif request.user.role.name == 'driver':
            if action == 'start_delivery':
                loader_id = request.POST.get('loader')
                order.loader = Loader.objects.get(id=loader_id)
                order.driver = request.user
                order.status = 'delivering'
                order.save()
                messages.success(request, "Доставка начата")

            elif action == 'complete_delivery':
                try:
                    with transaction.atomic():
                        for item in order.items.all():
                            product = item.product
                            if product.quantity < item.quantity:
                                raise Exception(f"Недостаточно {product.name}")
                            product.quantity -= item.quantity
                            product.save()
                        order.status = 'delivered'
                        order.save()
                        messages.success(request, "Доставка завершена")
                except Exception as e:
                    messages.error(request, str(e))

        return redirect('orders:detail', pk=order.id)
