from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BillPayment

class TransferForm(forms.Form):
    recipient_account = forms.CharField(max_length=20)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    message = forms.CharField(widget=forms.Textarea, required=False)

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=255, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'phone_number']

class TransferForm(forms.Form):
    receiver_account_number = forms.CharField(max_length=12, label="Receiver Account Number")
    amount = forms.DecimalField(max_digits=12, decimal_places=2, label="Amount")

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        label='Amount to Add'
    )

class BillPaymentForm(forms.ModelForm):
    class Meta:
        model = BillPayment
        fields = ['bill_category', 'bill_provider', 'bill_number', 'amount', 'due_date']

