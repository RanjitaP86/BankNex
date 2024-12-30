from django.contrib import admin
from .models import Account, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'balance')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'amount', 'status', 'timestamp')  # Use 'timestamp' instead of 'date'
    ordering = ('-timestamp',)  # Use 'timestamp' instead of 'date'
    list_filter = ('status', 'timestamp')  # Use 'timestamp' instead of 'date'
    search_fields = ('sender__user__username', 'receiver__user__username')
