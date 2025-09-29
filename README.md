🛍️ E-Commerce Website with PayPal Integration

This project is a full-featured e-commerce platform built using Django. It allows users to browse products, add them to a shopping cart, and securely complete purchases using PayPal payment gateway integration.

🚀 Features

✅ User Authentication: Secure login & registration system

✅ Product Catalog: Display products with details & images

✅ Shopping Cart: Add, update, or remove items before checkout

✅ Checkout System: Billing information collection

✅ PayPal Integration: Secure online payments with PayPal Sandbox/Live

✅ Order Tracking: Redirects to success/failure pages based on payment result

✅ Responsive UI: Works across devices

🛠️ Tech Stack

Backend: Django 5.x

Frontend: HTML, CSS, Bootstrap

Database: SQLite (can be switched to PostgreSQL/MySQL)

Payment Gateway: PayPal (via django-paypal)

Other Tools: Gunicorn, dj-database-url, NumPy, Matplotlib, OpenCV (for image processing utilities)

📦 Installation

Clone the repository:

git clone https://github.com/yourusername/ecom-paypal.git
cd ecom-paypal


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Run migrations:

python manage.py migrate


Create a superuser (for admin panel):

python manage.py createsuperuser


Run the server:

python manage.py runserver

💳 PayPal Setup

Create a PayPal Developer Account → PayPal Developer

Get your Sandbox Business Email and add it in settings.py:

PAYPAL_RECEIVER_EMAIL = "your-business-email@example.com"
PAYPAL_TEST = True  # Set to False for live payments


Update URLs in paypal_dict for success and failure redirects:

Success → /payment/success/

Failure → /payment/failed/

📂 Project Structure
ecom/
│── ecom/                # Project settings
│── payment/             # Payment app (PayPal integration)
│   │── views.py         # Checkout, success & failure views
│   │── urls.py          # Payment-related URLs
│── products/            # Product catalog app
│── templates/           # HTML templates (billing, success, failure)
│── static/              # CSS, JS, Images
│── requirements.txt     # Dependencies
│── manage.py
