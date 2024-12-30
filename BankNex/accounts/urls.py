# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts' # Set the application namespace
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('manage-accounts/', views.manage_accounts_view, name='manage_accounts'),
    path('transfer/', views.transfer_money_view, name='transfer_money'),
    path('transaction_history/', views.transaction_history_view, name='transaction_history'),
    path('bill-payment/', views.bill_payment_view, name='bill_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('add-money/', views.add_money_view, name='add_money'),
]
