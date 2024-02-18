from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Customer


def must_login(request):
    messages.error(request, 'Error, you must be logged in.')
    return redirect('login')


def home(request):
    if request.user.is_authenticated:
        customers = Customer.objects.all()
        return render(request, 'home.html', {'customers':customers})
    else:
        return redirect('login')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error, username or password incorrect.')
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    return redirect('home')


def customer_record(request, pk):
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(id=pk)
        except:
            messages.error(request, 'Customer doesn\'t exist.')
            return redirect('home')
        return render(request, 'customer.html', {'customer':customer})
    else:
        return must_login(request)
    

def delete_customer(request, pk):
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(id=pk)
        except:
            messages.error(request, 'Customer doesn\'t exist.')
            return redirect('home')
        customer.delete()
        messages.success(request, 'Customer deleted successfully.')
        return redirect('home')
    else:
        return must_login(request)


def add_customer(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            customer = Customer(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                address=request.POST['address'],
                city=request.POST['city'],
                state=request.POST['state'],
                zip_code=request.POST['zip_code']
            )
            customer.save()
            messages.success(request, 'Customer added successfully.')
            return redirect('home')
        else:
            return render(request, 'add_customer.html', {})
    else:
        return must_login(request)
    

def edit_customer(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            customer = Customer.objects.get(id=request.POST['id'])
            customer.first_name = request.POST['first_name']
            customer.last_name = request.POST['last_name']
            customer.email = request.POST['email']
            customer.phone = request.POST['phone']
            customer.address = request.POST['address']
            customer.city = request.POST['city']
            customer.state = request.POST['state']
            customer.zip_code = request.POST['zip_code']
            customer.save()
            messages.success(request, 'Customer edited successfully.')
            return redirect('home')
        else:
            try:
                customer = Customer.objects.get(id=pk)
            except:
                messages.error(request, 'Customer doesn\'t exist.')
                return redirect('home')
            return render(request, 'edit_customer.html', {'customer':customer})
    else:
        must_login()