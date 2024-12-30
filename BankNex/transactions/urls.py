from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('history/', views.transaction_history_view, name='transaction_history'),
]
