from Store.models import Product, Profile
from decimal import Decimal

class Cart():
    def __init__(self,request):
        self.session = request.session
        # Get request
        self.request= request

        #Get the current session key if it exists
        cart = self.session.get('cart')
        
        #if the user is new, no session key
        # if 'session_key' not in request.session:
        #     cart = self.session['session_key'] = {} 
        if cart is None:
            cart = self.session['cart']={}

            #Make sure cart is available on all pages of sites
            
        self.cart = cart
    
    def db_add(self,product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        #Logic
        if product_id in self.cart:
            # pass
            self.cart[product_id] += product_qty
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = (product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id= self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save the carty to the profile Model
            current_user.update(old_cart= str(carty))


    def add(self,product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        #Logic
        if product_id in self.cart:
            # pass
            self.cart[product_id] += product_qty
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = (product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id= self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save the carty to the profile Model
            current_user.update(old_cart= str(carty))


    def cart_total(self):
        # Get product id
        product_ids = self.cart.keys()
        # lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        # get qunatities
        quantities = self.cart
        # Start counting at 0
        total = Decimal("0.00")

        # for key, value in quantities.items():
        #     # convert keys string into int
        #     key = int(key)
        for product in products:
            qty = int(self.cart[str(product.id)])
            if product.is_sale:
                total = total + (product.sale_price * qty)
            else:
                total = total + (product.price * qty)
        
        return total


    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):

        #get ids from cart
        product_ids = self.cart.keys()

        #Use ids to lookup products in database model
        products = Product.objects.filter(id__in = product_ids)

        #Return those lookup products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self,product,quantity):
        product_id=str(product)
        product_qty=int(quantity)
        
        #Get cart
        ourcart = self.cart
        #Update Dic
        ourcart[product_id] = product_qty

        self.session.modified = True
        
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id= self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save the carty to the profile Model
            current_user.update(old_cart= str(carty))


        thing = self.cart
        return thing
    
    def delete(self,product):

        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id= self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save the carty to the profile Model
            current_user.update(old_cart= str(carty))