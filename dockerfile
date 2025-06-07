# Use Python 3.11 slim image as base
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    cron \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create crontab file

COPY cronfile /etc/cron.d/check_transactions

# Set permissions for crontab file
RUN chmod 0644 /etc/cron.d/check_transactions
# Create log file and set permissions
RUN touch /app/task.log 

# Copy project files
COPY . .





# Start cron service
RUN service cron start
RUN crontab /etc/cron.d/check_transactions

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the application
CMD ["service", "cron", "start", "&&", "gunicorn", "jevoucher.wsgi:application", "--bind", "0.0.0.0:8000"]
