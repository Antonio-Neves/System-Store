from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

    # Sales statistics
    today_sales = Sale.objects.filter(created_at__date=today)
    week_sales = Sale.objects.filter(created_at__date__gte=week_ago)
    month_sales = Sale.objects.filter(created_at__date__gte=month_ago)

    # Products with low stock
    low_stock_products = Product.objects.filter(stock__lte=F('min_stock'),
                                                active=True)

    # Best selling products
    best_sellers = Product.objects.annotate(
        total_sold=Sum('sale_items__quantity')
    ).order_by('-total_sold')[:5]

    context = {
        'total_products': Product.objects.filter(active=True).count(),
        'total_customers': Customer.objects.count(),
        'today_sales_count': today_sales.count(),
        'today_sales_total': today_sales.aggregate(Sum('total'))[
                                 'total__sum'] or 0,
        'week_sales_total': week_sales.aggregate(Sum('total'))[
                                'total__sum'] or 0,
        'month_sales_total': month_sales.aggregate(Sum('total'))[
                                 'total__sum'] or 0,
        'low_stock_products': low_stock_products,
        'best_sellers': best_sellers,
        'recent_sales': Sale.objects.all()[:10],
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
                             f'Product "{product.name}" created successfully!')
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
                             f'Product "{product.name}" updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'store/product_form.html',
                  {'form': form, 'action': 'Update', 'product': product})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.active = False
        product.save()
        messages.success(request,
                         f'Product "{product.name}" deleted successfully!')
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
                             f'Category "{category.name}" created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'store/category_form.html',
                  {'form': form, 'action': 'Create'})


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
                             f'Customer "{customer.name}" created successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'store/customer_form.html',
                  {'form': form, 'action': 'Create'})


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

    context = {
        'sales': sales[:50],
        'total': total,
        'average_ticket': average_ticket,
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

        if not product_ids:
            messages.error(request, 'Add at least one product to the sale!')
            return redirect('sale_create')

        # Create sale
        sale = Sale.objects.create(
            user=request.user,
            customer_id=customer_id if customer_id else None,
            payment_method=payment_method,
            discount=float(discount) if discount else 0
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
