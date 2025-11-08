# JeVoucher Setup Guide

## Recent Updates

This Django application has been updated with the following improvements:

### 1. Modern Tailwind CSS Styling
- Replaced Bootstrap with Tailwind CSS for a more modern, professional look
- All templates now use clean, gradient-based design with smooth animations
- Responsive design that works perfectly on mobile and desktop

### 2. Simplified Payment Flow
- **No email required**: Users no longer need to enter their email address during checkout
- A dummy email (configured in settings) is automatically used for Paystack transactions
- This streamlines the checkout process and reduces friction

### 3. Smart Phone Number Caching
- User phone numbers are automatically cached after the first transaction
- Phone numbers are remembered for 30 days using Django's caching framework
- Returning users will see their phone number pre-filled for convenience

## Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
USE_SQLITE=False
POSTGRES_DB=jevoucher
POSTGRES_USER=jevoucher
POSTGRES_PASSWORD=jevoucher_password
POSTGRES_HOST=db

# Paystack API Settings
PAYSTACK_SECRET_KEY=your-paystack-secret-key
PAYSTACK_PUBLIC_KEY=your-paystack-public-key

# Dummy Email for Transactions
# This email is used for all transactions so users don't need to provide their email
DUMMY_TRANSACTION_EMAIL=noreply@jevoucher.com

# SMS API Settings
SMS_API_KEY=your-sms-api-key
SMS_API_SENDER_ID=JeVoucher

# SSL/HTTPS Settings
ENABLE_SSL=False
```

## Installation Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create Cache Table** (for phone number caching)
   ```bash
   python manage.py createcachetable
   ```

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **Create Superuser** (if needed)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## Key Features

### Payment Flow
1. User selects a voucher duration plan
2. User enters only their phone number (no email required)
3. If the user has purchased before, their phone number is pre-filled
4. Payment is processed via Paystack using a dummy email
5. Voucher code is delivered via SMS immediately after successful payment

### Caching Implementation
- Phone numbers are cached using Django's database cache backend
- Cache key format: `user_phone_{session_key}`
- Cache timeout: 30 days (2,592,000 seconds)
- Session-based caching ensures privacy and security

### Tailwind CSS
The application now uses Tailwind CSS via CDN for rapid development and deployment.
All templates have been redesigned with:
- Modern gradient color schemes
- Smooth hover effects and transitions
- Responsive grid layouts
- Clean, professional UI components
- Accessible form elements

## Design System

### Color Palette
- **Primary Red**: `#dc2626` to `#7f1d1d` (red-600 to red-900)
- **Accent Orange**: `#f97316` to `#7c2d12` (orange-500 to orange-900)
- **Success Green**: `#10b981` (green-500)
- **Background**: Soft gradient from red-50 to orange-50

### Typography
- Font Family: Inter (Google Fonts)
- Font Weights: 300-900
- Clean, modern sans-serif design

## API Integration

### Paystack
- Uses Paystack Inline JS for seamless payment collection
- Supports Mobile Money (MTN, Vodafone, AirtelTigo) and Cards
- Currency: GHS (Ghana Cedis)
- Amount is multiplied by 100 (kobo conversion)

### SMS Delivery
- Voucher codes are sent immediately after successful payment
- SMS includes voucher code and validity period
- Sent to the phone number provided during checkout

## Database Schema

### Key Models
- **VoucherDuration**: Defines available plans (hours and pricing)
- **Voucher**: Individual voucher codes with status tracking
- **Transaction**: Payment records with customer details
- **VoucherFile**: For bulk voucher imports

### Caching
- Uses Django's database cache backend
- Cache table: `cache_table`
- Stores temporary user data (phone numbers)

## Security Notes

1. **Email Privacy**: Users don't provide personal emails, reducing data collection
2. **Session-Based Caching**: Phone numbers tied to sessions, not user accounts
3. **Secure Payments**: All transactions processed through Paystack's secure platform
4. **SSL Support**: Configure `ENABLE_SSL=True` in production

## Maintenance

### Cache Management
```bash
# Clear all cached data
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

### Database Cleanup
```bash
# Remove expired cache entries (automatic, but can be forced)
python manage.py clear_cache
```

## Troubleshooting

### Phone Number Not Caching
- Ensure `createcachetable` has been run
- Check that sessions are working properly
- Verify cache settings in `settings.py`

### Payment Issues
- Verify Paystack API keys are correct
- Check that callback URLs are accessible
- Ensure proper network connectivity

### SMS Not Sending
- Verify SMS API credentials
- Check phone number format
- Confirm SMS API balance

## Support

For issues or questions, please contact support or refer to the project documentation.

