# Ecommerce Application with Khalti Payment Gateway
This is an ecommerce web application built using Django and Tailwind CSS, integrated with the Khalti payment gateway for seamless online payments.

## Features
User registration and authentication

Product listing with categories and search functionality

Shopping cart and order management

Secure checkout process with Khalti payment gateway integration

Responsive design powered by Tailwind CSS

Admin dashboard for managing products, orders, and users

## Technologies Used
Backend: Django (Python web framework)

Frontend: Tailwind CSS for styling and responsiveness

Payment Gateway: Khalti API for secure payment processing

## Installation
Clone the repository:

```
git clone https://github.com/lucifervenom00/E-commerce-web-application-with-khalti-payment-gateway.git
cd E-commerce-web-application-with-khalti-payment-gateway
```
### Create and activate a virtual environment:

```
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```
### Install dependencies:

```
pip install -r requirements.txt
```
### Set up environment variables for Khalti payment gateway keys in .env file:

```
KHALTI_PUBLIC_KEY=your_khalti_public_key
KHALTI_SECRET_KEY=your_khalti_secret_key
```
### Apply migrations:

```
python manage.py migrate
```
### Collect static files:

```
python manage.py collectstatic
```
### Run the development server:

```
python manage.py runserver
```
### Open your browser and visit http://127.0.0.1:8000 to see the application in action.

## Usage
Browse products, add items to your cart, and proceed to checkout.

On checkout, choose Khalti as the payment method and complete payment securely.

Administrators can manage products and orders through the Django admin panel.

## Contribution
Contributions are welcome! Please fork the repository and submit pull requests for improvements or new features.

## License
This project is licensed under the MIT License.


