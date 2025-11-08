from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache

from sales.sms import SmsApi

from .models import VoucherDuration, Voucher, Transaction


class VoucherDurationListView(ListView):
    """View to display available voucher durations for purchase"""

    model = VoucherDuration
    template_name = "sales/voucher_duration_list.html"
    context_object_name = "durations"

    def get_queryset(self):
        return VoucherDuration.objects.filter(is_active=True)


class InitiatePaymentView(TemplateView):
    """View to initiate payment for a voucher"""

    template_name = "sales/initiate_payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        duration_id = self.request.GET.get("duration")
        if duration_id:
            duration = get_object_or_404(
                VoucherDuration, id=duration_id, is_active=True
            )
            context["duration"] = duration

        # Add Paystack public key to context
        context["paystack_public_key"] = settings.PAYSTACK_PUBLIC_KEY
        
        # Get cached phone number if available
        session_key = self.request.session.session_key
        if session_key:
            cached_phone = cache.get(f"user_phone_{session_key}")
            if cached_phone:
                context["cached_phone"] = cached_phone
        
        return context

    def post(self, request, *args, **kwargs):
        """
        Initiate payment transaction without requiring user email.
        Uses dummy email from settings and caches phone number for future use.
        """
        duration_id = request.POST.get("duration")
        phone = request.POST.get("phone")

        if not all([duration_id, phone]):
            return JsonResponse(
                {"status": "error", "message": "Duration and phone number are required"},
                status=400,
            )

        duration = get_object_or_404(VoucherDuration, id=duration_id, is_active=True)

        # Get an available voucher
        voucher = Voucher.objects.filter(
            status="available", duration=duration, transaction__isnull=True
        ).first()

        if not voucher:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "No vouchers available for this duration",
                },
                status=400,
            )

        # Use dummy email from settings
        dummy_email = settings.DUMMY_TRANSACTION_EMAIL
        
        # Cache phone number for this user session (expires in 30 days)
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cache.set(f"user_phone_{session_key}", phone, timeout=60*60*24*30)  # 30 days

        # Create transaction
        transaction = Transaction.objects.create(
            voucher=voucher,
            amount=duration.price,
            customer_email=dummy_email,
            customer_phone=phone,
        )

        # Initialize Paystack payment
        payment_data = {
            "reference": str(transaction.reference),
            "amount": float(transaction.amount) * 100,  # Paystack amount in kobo
            "email": dummy_email,
            "callback_url": request.build_absolute_uri(
                reverse("sales:verify_payment", args=[transaction.reference])
            ),
        }

        return JsonResponse({"status": "success", "payment_data": payment_data})


class VerifyPaymentView(TemplateView):
    """View to verify payment and deliver voucher"""

    template_name = "sales/payment_verification.html"

    def get(self, request, reference, *args, **kwargs):
        transaction = get_object_or_404(Transaction, reference=reference)

        # TODO: Verify payment with Paystack
        # This is a placeholder - implement actual Paystack verification

        # payment_verified = transaction.verify_payment()
        payment_verified = transaction.verify_payment()

        if payment_verified:
            transaction.status = "successful"
            transaction.save()

            # Mark voucher as sold
            transaction.get_voucher().mark_as_sold()

            # Calculate expiration time
            expires_at = timezone.now() + timezone.timedelta(
                hours=transaction.voucher.duration.duration_hours
            )
            transaction.voucher.expires_at = expires_at
            transaction.voucher.save()

            # Send SMS notification with voucher details
            sms_api = SmsApi()
            message = f"Your voucher code is {transaction.voucher.code}. Valid for {transaction.voucher.duration.duration_hours} hours."
            sms_api.send(
                recipients=[transaction.customer_phone],
                message=message,
                sender_id=settings.SMS_API_SENDER_ID,
            )

            return render(
                request,
                self.template_name,
                {"transaction": transaction, "status": "success"},
            )

        transaction.status = "failed"
        transaction.save()
        return render(
            request,
            self.template_name,
            {"transaction": transaction, "status": "failed"},
        )
