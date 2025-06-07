from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from sales.models import Transaction
from sales.sms import SmsApi
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Management command to check pending transactions and verify their payment status.
    This command:
    1. Finds transactions created in the last 10 minutes that are still pending
    2. Verifies their payment status with Paystack
    3. If payment is successful, sends SMS notification to the customer
    """

    help = "Checks pending transactions and verifies their payment status"

    def handle(self, *args, **options):
        # Get transactions from the last 10 minutes that are still pending
        self.stdout.write("[ ] Checking pending transactions")
        time_threshold = timezone.now() - timedelta(minutes=20)
        pending_transactions = Transaction.objects.filter(
            created_at__gte=time_threshold,
            created_at__lte=timezone.now() - timedelta(minutes=5),
            status="pending",
        )

        self.stdout.write(f"Found {pending_transactions.count()} pending transactions")

        for transaction in pending_transactions:
            try:
                self.stdout.write(
                    f"  [ ] Processing transaction {transaction.reference}"
                )
                # Verify payment with Paystack
                payment_verified = transaction.verify_payment()

                if payment_verified:
                    # Update transaction status
                    transaction.status = "successful"
                    transaction.save()

                    # Mark voucher as sold
                    voucher = transaction.get_voucher()
                    if voucher:
                        voucher.mark_as_sold()

                        # Calculate expiration time
                        expires_at = timezone.now() + timedelta(
                            hours=voucher.duration.duration_hours
                        )
                        voucher.expires_at = expires_at
                        voucher.save()

                        # Send SMS notification
                        if transaction.customer_phone:
                            sms_api = SmsApi()
                            message = f"Your voucher code is {voucher.code} \nValid for {voucher.duration.duration_hours} hours."
                            sms_sent = sms_api.send(
                                recipients=[transaction.customer_phone],
                                message=message,
                                sender_id=settings.SMS_API_SENDER_ID,
                            )

                            if sms_sent:
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f"    [✓] Successfully sent SMS for transaction {transaction.reference}"
                                    )
                                )
                            else:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f"    [x] Failed to send SMS for transaction {transaction.reference}"
                                    )
                                )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  [✓] Successfully verified payment for transaction {transaction.reference}"
                        )
                    )
                else:
                    # Mark transaction as failed if payment verification fails
                    self.stdout.write(
                        self.style.WARNING(
                            f"  [x] Payment verification failed for transaction {transaction.reference}"
                        )
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"  [x] Error processing transaction {transaction.reference}: {str(e)}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("[✓] Done validating all pending transactions")
        )
