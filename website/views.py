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
        customer = Customer.objects.get(id=pk)
        return render(request, 'customer.html', {'customer':customer})
    else:
        return must_login(request)
    

def delete_customer(request, pk):
    if request.user.is_authenticated:
        customer = Customer.objects.get(id=pk)
        customer.delete()
        messages.success(request, 'Customer deleted.')
        return redirect('home')
    else:
        return must_login(request)


def add_customer(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone = request.POST['phone']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip_code']
            customer = Customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code
            )
            customer.save()
            return redirect('home')
        else:
            return render(request, 'add_customer.html', {})
    else:
        return must_login(request)