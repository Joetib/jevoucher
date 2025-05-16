from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
import uuid

from sales.paystack import PayStack


class VoucherDuration(models.Model):
    """
    Model to manage different voucher durations and their prices
    """

    name = models.CharField(max_length=100)
    duration_hours = models.PositiveIntegerField(
        help_text="Duration in hours", validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.duration_hours} hours) - {self.price}"

    class Meta:
        ordering = ["duration_hours"]


class Voucher(models.Model):
    """
    Model to manage individual vouchers
    """

    STATUS_CHOICES = [
        ("available", "Available"),
        ("sold", "Sold"),
        ("used", "Used"),
        ("expired", "Expired"),
    ]

    code = models.CharField(max_length=50, unique=True)
    duration = models.ForeignKey(
        VoucherDuration, on_delete=models.PROTECT, related_name="vouchers"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sold_at = models.DateTimeField(null=True, blank=True)
    used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.status}"

    def mark_as_sold(self):
        """Mark voucher as sold and set sold timestamp"""
        self.status = "sold"
        self.sold_at = timezone.now()
        self.save()

    def mark_as_used(self):
        """Mark voucher as used and set used timestamp"""
        self.status = "used"
        self.used_at = timezone.now()
        self.save()

    def mark_as_expired(self):
        """Mark voucher as expired"""
        self.status = "expired"
        self.save()

    class Meta:
        ordering = ["-created_at"]


class Transaction(models.Model):
    """
    Model to track sales and payments
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("successful", "Successful"),
        ("failed", "Failed"),
    ]

    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    voucher = models.OneToOneField(
        Voucher, on_delete=models.PROTECT, related_name="transaction"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_reference = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference} - {self.status}"

    class Meta:
        ordering = ["-created_at"]

    def amount_value(self):
        return self.amount * 100

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.payment_reference, self.amount)
        if status:
            self.paystack_response = result
            if result["amount"] / 100 == self.amount:
                self.completed = True
            self.save()
            return True
        return False
