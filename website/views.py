from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Booking, UserProfile, ProductQuantity
from django.contrib import messages
from .forms import RegisterForm
from .booking_form import BookingForm,ProductForm


def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                user_profile = UserProfile.objects.get(user=user)
                usertype = user_profile.usertype
                request.session['usertype'] = usertype
            except UserProfile.DoesNotExist:
                usertype = 'unknown'
                request.session['usertype'] = 'unknown'

            messages.success(request, "You are logged in")
            return redirect('redirect_based_on_usertype')  # Redirect to the new URL
            
        else:
            messages.error(request, "Invalid username or password")
            return redirect('home')
    else:
        usertype = request.session.get('usertype', 'unknown')
        return render(request, 'home.html', {'usertype': usertype})


def redirect_based_on_usertype(request):
    usertype = request.session.get('usertype', 'unknown')

    if usertype == 'user':
        return redirect('user_dashboard')
    elif usertype == 'hospital':
        return redirect('hospital_dashboard')
    elif usertype == 'dispensory':
        return redirect('dispensary_dashboard')
    elif usertype == 'manufacturer':
        return redirect('manufacturer_dashboard')
    else:
        return redirect('home')



def logout_user(request):
    logout(request)
    messages.success(request, "you are logged out")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user= form.save()
            usertype = form.cleaned_data.get('usertype')
            UserProfile.objects.create(user=user, usertype=usertype)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You Have Successfully Registered! Welcome!")
                return redirect('home')
            else:
                messages.error(request, "There was an error with authentication.")
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})

def user_dashboard(request):
    return render(request, 'user.html')

def hospital_dashboard(request):
    return render(request, 'hospit.html')

def dispensary_dashboard(request):
    return render(request, 'disp.html')

def manufacturer_dashboard(request):
    return render(request, 'manufac.html')




@login_required
def add_product(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    usertype = user_profile.usertype  # Access the usertype field
    
    if usertype != 'manufacturer':
        return redirect('home')  # Redirect non-manufacturers to the home page
    else:
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save(manufacturer=user_profile)
            else:
                messages.error(request, "There was an error adding the product.")

        else:
            form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    product_quantities = ProductQuantity.objects.select_related('product', 'manufacturer')
    
    manufacturer_totals = {}
    for pq in product_quantities:
         if pq.manufacturer not in manufacturer_totals:
             manufacturer_totals[pq.manufacturer] = 0
         manufacturer_totals[pq.manufacturer] += pq.quantity

    context = {
        'products': products,
        'product_quantities': product_quantities,
         'manufacturer_totals': manufacturer_totals
    }
    return render(request, 'product_list.html', context)


@login_required
def book_product(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            manufacturer = form.cleaned_data['manufacturer']
            quantity = form.cleaned_data['quantity']
            
            try:
                product_quantity = ProductQuantity.objects.get(product=product, manufacturer=manufacturer)
                
                if product_quantity.quantity >= quantity:
                    # Deduct the quantity and save
                    product_quantity.quantity -= quantity
                    product_quantity.save()

                    # Create a booking record
                    Booking.objects.create(user=request.user, product=product, manufacturer=manufacturer, quantity=quantity)
                    
                    # Add a success message and redirect to the success page
                    messages.success(request, 'Product booked successfully!')
                    return redirect('success_page')
                else:
                    # Add an error message for insufficient stock
                    messages.error(request, 'Insufficient stock available.')
                    
            except ProductQuantity.DoesNotExist:
                # Add an error message for the non-existent product-manufacturer combination
                messages.error(request, 'The selected product and manufacturer combination does not exist.')
    else:
        form = BookingForm()
    
    # Render the booking form
    return render(request, 'book_product.html', {'form': form})

    
@login_required
def success_page(request):
    return render(request, 'success_page.html')