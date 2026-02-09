from django.shortcuts import render, get_object_or_404
from .models import Product, Category
import json
from django.http import JsonResponse
from django.utils import timezone


def homepage(request):
    products = Product.objects.all().order_by('category')
    categories = Category.objects.all()
    last_update = timezone.now()
    
    context = {
        'products': products,
        'categories': categories,
        'last_update': last_update
    }
    return render(request, 'products/homepage.html', context)


def filter_products(request):
    """AJAX endpoint to filter products by search query and category"""
    search_query = request.GET.get('search', '').strip()
    category_id = request.GET.get('category', '').strip()
    
    products = Product.objects.all()
    
    # Filter by search query
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Filter by category
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Build product data for JSON response
    product_data = []
    for product in products:
        product_data.append({
            'id': product.id,
            'name': product.name,
            'current_price': product.current_price,
            'previous_price': product.previous_price,
            'image_url': product.image_url if product.image_url else None,
            'category_name': product.category.name,
            'url': f'/product/{product.pk}/'
        })
    
    return JsonResponse({'products': product_data})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Siapkan data untuk Chart.js
    # Format: label (tanggal), data (harga)
    from datetime import timedelta
    seven_days_ago = timezone.now() - timedelta(days=7)
    history_data = product.history.filter(recorded_at__gte=seven_days_ago).order_by('recorded_at')
    
    dates = [h.recorded_at.strftime("%Y-%m-%d") for h in history_data]
    prices = [h.price for h in history_data]

    context = {
        'product': product,
        'chart_dates': json.dumps(dates),
        'chart_prices': json.dumps(prices),
    }
    return render(request, 'products/product_detail.html', context)
