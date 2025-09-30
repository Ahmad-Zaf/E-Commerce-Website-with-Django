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

ScreenShots-

### Home Page  
![Home Page](https://github.com/Ahmad-Zaf/E-Commerce-Website-with-Django/blob/main/Screenshot/1)Home_page.png?raw=true)

### Upload MCQ Sheet  
![Upload MCQ sheet](https://github.com/Ahmad-Zaf/E-Assessment-using-Image-Processing/blob/main/eassesment%20code/Asset/Upload%20MCQ%20sheet.png?raw=true)  

### Compare Answers  
![Compare Answers](https://github.com/Ahmad-Zaf/E-Assessment-using-Image-Processing/blob/main/eassesment%20code/Asset/Compare%20Answers.png?raw=true)  

### Mark Graph  
![Mark Graph](https://github.com/Ahmad-Zaf/E-Assessment-using-Image-Processing/blob/main/eassesment%20code/Asset/Mark%20graph.png?raw=true)  

### Enter Student Name  
![Enter Student Name](https://github.com/Ahmad-Zaf/E-Assessment-using-Image-Processing/blob/main/eassesment%20code/Asset/Enter%20Student%20Name.png?raw=true)  

Update URLs in paypal_dict for success and failure redirects:

Success → /payment/success/

Failure → /payment/failed/
