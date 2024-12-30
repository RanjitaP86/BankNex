from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import TransferForm, CustomLoginForm,DepositForm,BillPaymentForm
from django.contrib import messages
from .forms import CustomUserCreationForm,TransferForm
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from django.db.models import Q

def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request.POST)  # Use request.POST instead of data=request.POST

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate user using username and password (phone number not used for authentication here)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect to the dashboard after successful login
                return redirect('accounts:dashboard')  # Redirect to the dashboard
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('accounts:login')  
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')  # Make sure this matches the name of your login URL
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_money_view(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = request.user.account
            account.deposit(amount)
            messages.success(request, f"${amount} has been added to your account successfully!")
            return redirect('accounts:dashboard')
    else:
        form = DepositForm()
    return render(request, 'accounts/add_money.html', {'form': form})

@login_required
def dashboard_view(request):
    try:
        account_number = request.user.account.account_number
        balance = request.user.account.balance
    except Account.DoesNotExist:
        # Handle the case where the profile doesn't exist
        account_number = None
        balance = None
        messages.error(request, "Your profile does not exist. Please contact support.")
    
    return render(request, 'accounts/dashboard.html', {'account_number': account_number, 'balance': balance})

@login_required
def manage_accounts_view(request):
    # Logic for managing user accounts (e.g., showing account balance, account settings)
    account_number = request.user.account.account_number
    balance = request.user.account.balance
    
    # Pass account details to the template context
    context = {
        'account_number': account_number,
        'balance': balance,
    }
    return render(request, 'accounts/manage_accounts.html', context)


@login_required
def transfer_money_view(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            receiver_account_number = form.cleaned_data['receiver_account_number']
            amount = form.cleaned_data['amount']

            try:
                # Fetch sender and receiver accounts
                sender = request.user.account
                receiver = get_object_or_404(Account, account_number=receiver_account_number)

                if sender == receiver:
                    messages.error(request, "You cannot transfer money to your own account.")
                    return redirect('accounts:transfer_money')

                if sender.balance < amount:
                    messages.error(request, "Insufficient balance for this transaction.")
                else:
                    # Perform transaction
                    sender.balance -= amount
                    receiver.balance += amount
                    sender.save()
                    receiver.save()

                    # Log the transaction
                    Transaction.objects.create(
                        sender=sender,
                        receiver=receiver,
                        amount=amount,
                        status='Completed',
                        description='Money Transfer'
                    )

                    messages.success(request, f"${amount} successfully transferred to {receiver.user.username}.")
                    return redirect('accounts:dashboard')
            
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('accounts:transfer_money')
    else:
        form = TransferForm()

    return render(request, 'accounts/transfer.html', {'form': form})


@login_required
def transaction_history_view(request):
    transactions = Transaction.objects.filter(
        Q(sender__user=request.user) | Q(receiver__user=request.user)
    ).order_by('-timestamp')  # Order by date or timestamp, newest first
       
    return render(request, 'accounts/transaction_history.html', {'transactions': transactions})

def bill_payment_view(request):
    if request.method == 'POST':
        form = BillPaymentForm(request.POST)
        if form.is_valid():
            bill_payment = form.save(commit=False)
            bill_payment.user = request.user  # Attach logged-in user
            bill_payment.save()
            return redirect(('accounts:payment_success'))  # Redirect to a success page or confirmation page
    else:
        form = BillPaymentForm()
    
    return render(request, 'accounts/bill_payment.html', {'form': form})

def payment_success(request):
    return render(request, 'accounts/payment_success.html')

@login_required
def logout_view(request):
    return render(request, 'home.html')


