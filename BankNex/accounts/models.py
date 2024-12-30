from django.db import models
from django.contrib.auth.models import User
import random
from django.utils import timezone

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=12, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def generate_account_number(self):
        """ Generate a unique account number when an account is created. """
        while True:
            account_number = str(random.randint(1000000000, 9999999999))  # A random 10-digit number
            if not Account.objects.filter(account_number=account_number).exists():
                break
        return account_number

    def save(self, *args, **kwargs):
        """ Ensure an account number is assigned before saving the account. """
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    def deposit(self, amount):
        self.balance += amount
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Account"

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    sender = models.ForeignKey('Account', related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey('Account', related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    timestamp = models.DateTimeField(default=timezone.now)  # Use 'timestamp' instead of 'date'

    def __str__(self):
        return f"{self.sender.user.username} -> {self.receiver.user.username}: ${self.amount} - {self.status}"
    

class BillPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill_category = models.CharField(max_length=255)
    bill_provider = models.CharField(max_length=255)
    bill_number = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.bill_category} - {self.bill_provider} - {self.status}"
