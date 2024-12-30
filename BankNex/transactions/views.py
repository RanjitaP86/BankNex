from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transaction
from django.core.paginator import Paginator

@login_required
def transaction_history_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        transactions = transactions.filter(date__range=[start_date, end_date])

    # Pagination
    paginator = Paginator(transactions, 10)  # Show 10 transactions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'transactions': page_obj,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'transactions/transaction_history.html', context)
