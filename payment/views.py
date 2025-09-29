from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.models import ShippingAddress, Order, OrderItem
from payment.forms import ShippingForm, PaymentForm
from django.contrib.auth.models import User
from django.contrib import messages
from Store.models import Product, Profile
import datetime

# import paypal
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid


from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid

def store(request):
    # Fetch all products (or filter by category if needed)
    products = Product.objects.all()
    
    # Optional: fetch categories for filtering/navigation
    categories = Category.objects.all()
    
    # Optional: implement search/filter
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)
    
    # Pass data to template
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'store.html', context)


def orders(request,pk ):
    if request.user.is_authenticated and request.user.is_superuser:

        order = Order.objects.get(id=pk)
        
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            # Check if true or false
            if status == "true":
                order = Order.objects.filter(id=pk)
                # Update status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order = Order.objects.filter(id=pk)
                # Update status
                order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('home')

        
        return render(request, "payment/orders.html", {"order":order,"items":items})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            
            order = Order.objects.filter(id=num)

            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)
            
            messages.success(request, "Shipping Status Updated")
            return redirect('home')

        return render(request, "payment/not_shipped_dash.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']

            order = Order.objects.filter(id=num)

            now = datetime.datetime.now()
            order.update(shipped=False)
            
            messages.success(request, "Shipping Status Updated")
            return redirect('home')

        return render(request, "payment/shipped_dash.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get billing Info from the last page
        payment_form = PaymentForm(request.POST or None )
        # Get shipping session data
        my_shipping = request.session.get('my_shipping')
        
        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        
        # Create shipping address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        if request.user.is_authenticated:
            # logged in
            user = request.user
            create_order = Order(user= user, full_name= full_name, email= email, shipping_address= shipping_address, amount_paid= amount_paid)
            create_order.save()

            # Add order item
            # Get the order ID
            order_id = create_order.pk

            # Get product ID
            for product in cart_products():
                # Get product id
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # value
                        create_order_item = OrderItem(order_id= order_id ,product_id= product_id ,user= user ,quantity= value ,price= price)
                        create_order_item.save()

                # Delete our cart
                # for key in list(request.session.keys()):
                #     if key == "session_key":
                #         del request.session[key] 
                # cart.clear()
                if "cart" in request.session:
                    del request.session["cart"]
                    request.session.modified = True

            messages.success(request, "Order Placed!")
            return redirect('home')
        else:
            # Not logged in
            create_order = Order(full_name= full_name, email= email, shipping_address= shipping_address, amount_paid= amount_paid)
            create_order.save()

            # Add order item
            # Get the order ID
            order_id = create_order.pk

            # Get product ID
            for product in cart_products():
                # Get product id
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # value
                        create_order_item = OrderItem(order_id= order_id ,product_id= product_id ,quantity= value ,price= price)
                        create_order_item.save()

                # Delete our cart
                for key in list(request.session.keys()):
                    if key == "session_key":
                        del request.session[key]

                # Delete our old cart
                current_user = Profile.objects.filter(user__id=request.user.id)

                current_user.update(old_cart="")
                 
            messages.success(request, "Order Placed!")
            return redirect('home')
        

    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def billing_info(request):
    if request.POST:

        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        host= request.get_host()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount' : totals ,
            'item_name' : 'PRODUCTS',
            'no_shipping': '2',
            'invoice' : str(uuid.uuid4()),
            'currency_code' : 'USD',
            'notify_url' : 'https://{}{}'.format(host, reverse("paypal-ipn")),
            'return_url' : 'https://{}{}'.format(host, reverse("payment_success")),
            'cancel_return' : 'https://{}{}'.format(host, reverse("payment_failed")), 
        }

        # Create actual paypal button
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

        if request.user.is_authenticated:

            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {
                'paypal_form':paypal_form,
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_info": request.POST,
                "billing_form":billing_form,
            })
        
        else:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {
                "paypal_form":paypal_form,
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_info": request.POST,
                "billing_form":billing_form,
            })


        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
            "shipping_form": shipping_form,
        })
    else:
        messages.success(request, "Add Products in Cart")
        return redirect('home')


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    
    if request.user.is_authenticated:

        shipping_user, created = ShippingAddress.objects.get_or_create(user = request.user) 
        
        shipping_form= ShippingForm(request.POST or None, instance = shipping_user)
        
        return render(request, "payment/checkout.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "shipping_form": shipping_form,
    })
    else:
         
        shipping_form= ShippingForm(request.POST or None)

        return render(request, "payment/checkout.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "shipping_form": shipping_form,
    })
   


def payment_success(request):
    return render(request, "payment/payment_success.html", {})

def payment_failed(request):
    return render(request, "payment/payment_failed.html", {})
