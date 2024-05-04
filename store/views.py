# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

def category(request, space):
        # Replace Hyphens with Spaces
        space = space.replace('-', ' ')
        # Grab the category from the url
        try:
            # Look Up The Category
            category = Category.objects.get(name=space)
            products = Product.objects.filter(category=category)
            total_quantity = 0
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user)
                total_quantity = sum(item.quantity for item in cart_items)
            context = {
                 'products':products, 
                 'category':category,
                 'total_quantity':total_quantity
            }
            
            return render(request, 'categories/category.html', context)
        except:
            messages.success(request, ("That Category Doesn't Exist..."))
            return redirect('home')

def category_summary(request):
    categories = Category.objects.all()
    total_quantity = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_quantity = sum(item.quantity for item in cart_items)

    context = {
         "categories":categories,
         'total_quantity':total_quantity         
    }
    return render(request, 'categories/category_summary.html', context)	

def product(request,pk):
    product = Product.objects.get(id=pk)
    total_quantity = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_quantity = sum(item.quantity for item in cart_items)

    context = {
         'product':product,
         'total_quantity':total_quantity         
    }

    return render(request, 'myapp/product.html',context)


def home(request):
    products = Product.objects.all()
    total_quantity = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_quantity = sum(item.quantity for item in cart_items)

    context = {
        'products': products,
        'total_quantity': total_quantity
    }
    return render(request, 'myapp/home.html', context)
     

@login_required
def view_cart(request):
	cart_items = CartItem.objects.filter(user=request.user)
	total_price = sum(item.product.price * item.quantity for item in cart_items)
	total_quantity = sum(1 * item.quantity for item in cart_items)
	context = {
		'cart_items': cart_items, 
		'total_price': total_price,
		'total_quantity': total_quantity,
		}
	return render(request, 'myapp/cart.html', context)

@login_required
def add_to_cart(request, product_id):
	product = Product.objects.get(id=product_id)
	cart_item, created = CartItem.objects.get_or_create(product=product, 
													user=request.user)
	cart_item.quantity += 1
	cart_item.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_from_cart(request, item_id):
	cart_item = CartItem.objects.get(id=item_id)
	if cart_item.quantity > 1:
		cart_item.quantity -= 1
		cart_item.save()
    		
	else:
		cart_item.delete()
	return redirect('view_cart')

@login_required
def checkout(request):
        
        # This is only for storing the customer information for shipping
        if request.method == 'POST':
            data = request.POST
            name = data['name']
            email = data['email']
            phone = data['phone']
            address = data['address']
            city = data['city']
            state = data['state']
            Customer.objects.create(name=name, email=email, phone=phone, address=address, city=city, state=state)

        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        
        total_quantity = sum(1 * item.quantity for item in cart_items)
        context = {
            'cart_items': cart_items, 
            'total_price': total_price,
            'total_quantity': total_quantity,
            }
        
        
        return render(request, 'myapp/checkout.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        # Item already in wishlist
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist')

@login_required
def wishlist_view(request):
	wishlist_items = WishlistItem.objects.filter(user=request.user)
	cart_items = CartItem.objects.filter(user=request.user)
	total_quantity = sum(item.quantity for item in cart_items)
	context = {
		'wishlist_items': wishlist_items,
		'total_quantity': total_quantity,
		}
	return render(request, 'myapp/wishlist.html', context)


# auth views
 
def register(request):
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name',"name is not found")
        last_name = data['last_name']
        username = data['username']
        email = data['email']
        password = data['password']
        password1 = data['password1']

        if(password==password1):
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username already exists!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already exists!')
                return redirect('register')
            else:
                User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                messages.success(request,'Registered successfully!')
                return redirect('login')

        else:
            messages.error(request, "Password doesn't match")
            return redirect('register')


    return render(request, 'auth/register.html')


def log_in(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        
        
        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request, "Successfully logged in")
            return redirect('home')
            

        
        else:
            messages.error(request,"Username or Password didn't match")
            return redirect('login')
        
    return render(request,'auth/login.html')

def log_out(request):
    # Clear the user's cart items
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items.delete()

    logout(request)
    return redirect('login')

@login_required(login_url='login')
def change_password(request):
    cf = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        cf = PasswordChangeForm(user=request.user, data=request.POST)
        if cf.is_valid():   #for validation
            cf.save()
            return redirect('login')
    return render(request,'auth/change_password.html',{'cf':cf})


