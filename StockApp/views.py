from django.shortcuts import render
from django.db.models import Sum, F
from .models import Stock
from django.http import JsonResponse
# Create your views here.


def stock_stats_view(request):
    total_books = Stock.objects.count()
    total_quantity = Stock.objects.aggregate(total=Sum('quantity'))['total'] or 0
    total_low_stock = Stock.objects.filter(quantity__lte=F('min_quantity')).count()
    total_out_of_stock = Stock.objects.filter(quantity=0).count()
    top_books = Stock.objects.order_by('-quantity')[:5]

    context = {
        'total_books': total_books,
        'total_quantity': total_quantity,
        'total_low_stock': total_low_stock,
        'total_out_of_stock': total_out_of_stock,
        'top_books': top_books,
    }
    return render(request, 'stock/stats.html', context)

def stock_stats_data(request):
    """
    Returns JSON aggregated data for charts.
    Example: total quantity per category. Adapt the aggregation to your needs.
    """
    # Group by category and sum quantity
    qs = (
        Stock.objects
        .select_related('book')
        .values('book__genre')
        .annotate(total=Sum('quantity'))
        .order_by('-total')
    )

    labels = [row['book__genre'] or 'Unknown' for row in qs]
    data = [int(row['total'] or 0) for row in qs]

    totals = {
        'total_books': Stock.objects.count(),
        'total_quantity': int(Stock.objects.aggregate(total=Sum('quantity'))['total'] or 0),
        'total_low_stock': Stock.objects.filter(quantity__lte=F('min_quantity')).count(),
        'total_out_of_stock': Stock.objects.filter(quantity=0).count(),
    }

    return JsonResponse({
        'labels': labels,
        'data': data,
        'title': 'Stock quantity by genre',
        'totals': totals
    })