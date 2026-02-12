from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import timedelta
from .models import Product, Category, Customer, Sale, SaleItem, StockMovement
from .forms import ProductForm, CategoryForm, CustomerForm, SaleForm, \
    StockMovementForm


@login_required
def dashboard(request):
    # Get statistics
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    year_start = today.replace(month=1, day=1)

    # Sales statistics - ONLY COMPLETED SALES (excluding canceled)
    today_sales = Sale.objects.filter(created_at__date=today,
                                      status='completed')
    week_sales = Sale.objects.filter(created_at__date__gte=week_ago,
                                     status='completed')
    month_sales = Sale.objects.filter(created_at__date__gte=month_ago,
                                      status='completed')
    year_sales = Sale.objects.filter(created_at__date__gte=year_start,
                                     status='completed')

    # Products with low stock
    low_stock_products = Product.objects.filter(stock__lte=F('min_stock'),
                                                active=True)

    # Best-selling products - ONLY from completed sales
    best_sellers = Product.objects.annotate(
        total_sold=Sum('sale_items__quantity',
                       filter=Q(sale_items__sale__status='completed'))
        # ← ADDED filter
    ).order_by('-total_sold')[:5]

    # Calculate profits
    def calculate_profit(sales_queryset):
        total_profit = 0
        for sale in sales_queryset:
            for item in sale.items.all():
                profit_per_item = (item.price - item.product.cost) * item.quantity
                total_profit += profit_per_item
        return total_profit

    today_profit = calculate_profit(today_sales)
    week_profit = calculate_profit(week_sales)
    month_profit = calculate_profit(month_sales)
    year_profit = calculate_profit(year_sales)

    context = {
        'today_sales_total': today_sales.aggregate(
            total_com_desconto=Sum(F('total') - F('discount'))
        )['total_com_desconto'] or 0,
        'today_profit': today_profit,
        'week_sales_total': week_sales.aggregate(Sum('total'))[
                                'total__sum'] or 0,
        'week_profit': week_profit,
        'month_sales_total': month_sales.aggregate(Sum('total'))[
                                 'total__sum'] or 0,
        'month_profit': month_profit,
        'year_sales_total': year_sales.aggregate(Sum('total'))[
                                'total__sum'] or 0,
        'year_profit': year_profit,
        'low_stock_products': low_stock_products,
        'best_sellers': best_sellers,
        'recent_sales': Sale.objects.all()[:10],
        # Shows all (including canceled for history)
    }

    return render(request, 'store/dashboard.html', context)


# PRODUCT VIEWS
@login_required
def product_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    products = Product.objects.filter(active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(barcode__icontains=query) |
            Q(description__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    }

    return render(request, 'store/product_list.html', context)


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request,
                             f'Produto "{product.name}" criado com sucesso!')
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'store/product_form.html',
                  {'form': form, 'action': 'Create'})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,
                             f'Produto "{product.name}" alterado com sucesso!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'store/product_form.html',
                  {'form': form, 'action': 'Alterar', 'product': product})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.active = False
        product.save()
        messages.success(request,
                         f'Produto "{product.name}" eliminado com sucesso!')
        return redirect('product_list')

    return render(request, 'store/product_confirm_delete.html',
                  {'product': product})


# CATEGORY VIEWS
@login_required
def category_list(request):
    categories = Category.objects.annotate(product_count=Count('products'))
    return render(request, 'store/category_list.html',
                  {'categories': categories})


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request,
                             f'Categoria "{category.name}" creada com sucesso!')
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'store/category_form.html',
                  {'form': form, 'action': 'Criar'})


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request,
                             f'Categoria "{category.name}" atualizada com sucesso!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'store/category_form.html',
                  {'form': form, 'action': 'Editar', 'category': category})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request,
                         f'Categoria "{category_name}" excluída com sucesso!')
        return redirect('category_list')

    return render(request, 'store/category_confirm_delete.html',
                  {'category': category})


# CUSTOMER VIEWS
@login_required
def customer_list(request):
    query = request.GET.get('q', '')
    customers = Customer.objects.all()

    if query:
        customers = customers.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query) |
            Q(cpf__icontains=query)
        )

    return render(request, 'store/customer_list.html',
                  {'customers': customers, 'query': query})


@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request,
                             f'Cliente "{customer.name}" criado com sucesso!')
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'store/customer_form.html',
                  {'form': form, 'action': 'Criar'})


@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request,
                             f'Customer "{customer.name}" updated successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'store/customer_form.html',
                  {'form': form, 'action': 'Update', 'customer': customer})


# SALE VIEWS
@login_required
def sale_list(request):
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    sales = Sale.objects.all()

    if date_from:
        sales = sales.filter(created_at__date__gte=date_from)

    if date_to:
        sales = sales.filter(created_at__date__lte=date_to)

    total = sales.aggregate(Sum('total'))['total__sum'] or 0
    sales_count = sales.count()
    average_ticket = total / sales_count if sales_count > 0 else 0

    # Calculate profit
    total_profit = 0
    for sale in sales:
        for item in sale.items.all():
            profit_per_item = (item.price - item.product.cost) * item.quantity
            total_profit += profit_per_item

    context = {
        'sales': sales[:50],
        'total': total,
        'average_ticket': average_ticket,
        'total_profit': total_profit,  # NEW
        'date_from': date_from,
        'date_to': date_to,
    }

    return render(request, 'store/sale_list.html', context)


@login_required
def sale_create(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_id')
        quantities = request.POST.getlist('quantity')
        customer_id = request.POST.get('customer')
        payment_method = request.POST.get('payment_method')
        discount = request.POST.get('discount', 0)
        notes = request.POST.get('notes', '')

        if not product_ids:
            messages.error(request, 'Add at least one product to the sale!')
            return redirect('sale_create')

        # Create sale
        sale = Sale.objects.create(
            user=request.user,
            customer_id=customer_id if customer_id else None,
            payment_method=payment_method,
            discount=float(discount) if discount else 0,
            notes = request.POST.get('notes', '')
        )

        total = 0

        # Add items to sale
        for prod_id, qty in zip(product_ids, quantities):
            if prod_id and qty:
                product = Product.objects.get(id=prod_id)
                quantity = int(qty)

                if product.stock < quantity:
                    messages.error(request,
                                   f'Insufficient stock for {product.name}!')
                    sale.delete()
                    return redirect('sale_create')

                # Create sale item
                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )

                # Update stock
                product.stock -= quantity
                product.save()

                # Create stock movement
                StockMovement.objects.create(
                    product=product,
                    movement_type='out',
                    quantity=quantity,
                    reason=f'Sale #{sale.id}',
                    user=request.user
                )

                total += product.price * quantity

        sale.total = total
        sale.save()

        messages.success(request, f'Sale #{sale.id} created successfully!')
        return redirect('sale_detail', pk=sale.id)

    products = Product.objects.filter(active=True, stock__gt=0)
    customers = Customer.objects.all()

    context = {
        'products': products,
        'customers': customers,
        'payment_methods': Sale.PAYMENT_METHODS,
    }

    return render(request, 'store/sale_form.html', context)


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'store/sale_detail.html', {'sale': sale})


@login_required
def sale_cancel(request, pk):
    sale = get_object_or_404(Sale, pk=pk)

    # Check if already cancelled
    if sale.is_cancelled:
        messages.error(request, 'Esta venda já está cancelada!')
        return redirect('sale_detail', pk=pk)

    if request.method == 'POST':
        password = request.POST.get('password')
        reason = request.POST.get('reason', '')

        # Authenticate superuser
        user = authenticate(username=request.user.username, password=password)

        if user is None or not user.is_superuser:
            messages.error(request,
                           'Senha incorreta ou usuário sem permissão de superuser!')
            return render(request, 'store/sale_cancel.html', {'sale': sale})

        # Cancel sale
        sale.status = 'cancelled'
        sale.cancelled_at = timezone.now()
        sale.cancellation_reason = reason
        sale.cancelled_by = request.user
        sale.save()

        # Return stock
        for item in sale.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()

            # Create stock movement
            StockMovement.objects.create(
                product=product,
                movement_type='in',
                quantity=item.quantity,
                reason=f'Cancelamento da Venda #{sale.id} - {reason}',
                user=request.user
            )

        messages.success(request,
                         f'Venda #{sale.id} cancelada com sucesso! Estoque devolvido.')
        return redirect('sale_detail', pk=pk)

    return render(request, 'store/sale_cancel.html', {'sale': sale})


# STOCK VIEWS
@login_required
def stock_movements(request):
    product_id = request.GET.get('product', '')
    movements = StockMovement.objects.all()

    if product_id:
        movements = movements.filter(product_id=product_id)

    products = Product.objects.filter(active=True)

    context = {
        'movements': movements[:100],
        'products': products,
        'selected_product': product_id,
    }

    return render(request, 'store/stock_movements.html', context)


@login_required
def stock_adjustment(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.user = request.user
            movement.save()

            # Update product stock
            product = movement.product
            if movement.movement_type == 'in':
                product.stock += movement.quantity
            elif movement.movement_type == 'out':
                product.stock -= movement.quantity
            elif movement.movement_type == 'adjustment':
                product.stock = movement.quantity

            product.save()

            messages.success(request, 'Stock updated successfully!')
            return redirect('stock_movements')
    else:
        form = StockMovementForm()

    return render(request, 'store/stock_adjustment.html', {'form': form})


# Receipt views
@login_required
def sale_receipt(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'store/sale_receipt.html', {'sale': sale})
