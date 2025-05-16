# JeVoucher - WiFi Voucher Management System

JeVoucher is a modern web application for selling and managing WiFi vouchers. Built with Django and featuring a beautiful, responsive UI, it provides a seamless experience for both administrators and customers.

## Features

- 🎫 **Voucher Management**
  - Create and manage WiFi vouchers with different durations
  - Automatic voucher generation and validation
  - Secure voucher delivery via email

- 💳 **Payment Integration**
  - Integrated with Paystack for secure payments
  - Support for Mobile Money and Card payments
  - Real-time payment verification

- 🎨 **Modern UI/UX**
  - Responsive design that works on all devices
  - Beautiful animations and transitions
  - Intuitive user interface

- 🔒 **Security**
  - Secure payment processing
  - Email verification
  - Protected admin interface

## Tech Stack

- **Backend**: Django 4.2
- **Frontend**: 
  - Bootstrap 5
  - Custom CSS with modern animations
  - JavaScript for interactive features
- **Payment**: Paystack API
- **Email**: Django's email backend

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jevoucher.git
cd jevoucher
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Configuration

### Required Environment Variables

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `PAYSTACK_SECRET_KEY`: Your Paystack secret key
- `PAYSTACK_PUBLIC_KEY`: Your Paystack public key
- `EMAIL_HOST`: SMTP host
- `EMAIL_PORT`: SMTP port
- `EMAIL_HOST_USER`: SMTP username
- `EMAIL_HOST_PASSWORD`: SMTP password

### Optional Environment Variables

- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `CSRF_TRUSTED_ORIGINS`: Comma-separated list of trusted origins

## Usage

### Admin Interface

1. Access the admin interface at `/admin`
2. Log in with your superuser credentials
3. Manage vouchers, users, and transactions

### Customer Flow

1. Visit the homepage
2. Select a voucher duration
3. Enter email and phone number
4. Complete payment via Paystack
5. Receive voucher via email

## Development

### Project Structure

```
jevoucher/
├── manage.py
├── requirements.txt
├── .env.example
├── jevoucher/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── sales/
    ├── models.py
    ├── views.py
    ├── urls.py
    └── templates/
        └── sales/
            ├── base.html
            ├── voucher_list.html
            └── payment_verification.html
```

### Running Tests

```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email support@jevoucher.com or create an issue in the repository.

## Acknowledgments

- Django Documentation
- Paystack API Documentation
- Bootstrap Documentation 