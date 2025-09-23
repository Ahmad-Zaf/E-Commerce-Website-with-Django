from django.shortcuts import render , get_object_or_404
from .cart import Cart
from Store.models import Product
from django.http import JsonResponse
from django.contrib import messages 


def cart_summary(request):

    #get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, "cart/cart_summary.html", { "cart_products": cart_products, "quantities": quantities, "totals":totals })

def cart_add(request):
    #Get the cart
    cart = Cart(request)
    #test for post
    if request.POST.get('action') == 'post':

        #Get Product
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        #lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        #save to session
        cart.add(product=product, quantity=product_qty)

        #GetCart Quantity
        cart_quantity = cart.__len__()

        #Return responce
        #response = JsonResponse({'Product Name :': product.name})
        response = JsonResponse({ 'qty': cart_quantity })
        messages.success(request, ("Product Added To Cart..."))
        return response

def cart_delete(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        #Get Product
        product_id = int(request.POST.get('product_id'))
        # Call delete function in cart
        cart.delete(product=product_id)
        
        reponse = JsonResponse({'product':product_id})
        # return redirected(cart_summary)
        messages.success(request, ("Product Deleted From Cart..."))
        return reponse


def cart_update(request):

    cart = Cart(request)
    
    if request.POST.get('action') == 'post':

        #Get Product
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        reponse = JsonResponse({'qty':product_qty})
        messages.success(request, ("Cart Updated..."))
        return reponse
    
