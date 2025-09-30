from django.urls import path, include
from . import views

urlpatterns = [

    path('payment/payment_success', views.payment_success, name ='paypal_success'),
    path('payment/payment_failed', views.payment_failed, name ='paypal_failed'),
    path('checkout', views.checkout, name ='checkout'),
    path('billing_info', views.billing_info, name ='billing_info'),
    path('process_order', views.process_order, name ='process_order'),
    path('shipped_dash', views.shipped_dash, name ='shipped_dash'),
    path('not_shipped_dash', views.not_shipped_dash, name ='not_shipped_dash'),
    path('orders/<int:pk>', views.orders, name='orders'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('orders/history/', views.order_history, name='order_history'),
    path('', views.store, name="store"),

]
