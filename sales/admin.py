from django.contrib import admin
from django.contrib import messages
from .models import VoucherDuration, Voucher, Transaction, VoucherFile
import csv


@admin.register(VoucherDuration)
class VoucherDurationAdmin(admin.ModelAdmin):
    list_display = ("name", "duration_hours", "price", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "duration",
        "status",
        "created_at",
        "sold_at",
        "used_at",
        "expires_at",
    )
    list_filter = ("status", "duration")
    search_fields = ("code",)
    readonly_fields = ("created_at", "sold_at", "used_at")
    actions = ["mark_as_expired"]

    def mark_as_expired(self, request, queryset):
        for voucher in queryset:
            voucher.mark_as_expired()
        self.message_user(request, f"{queryset.count()} vouchers marked as expired.")

    mark_as_expired.short_description = "Mark selected vouchers as expired"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "voucher",
        "amount",
        "status",
        "customer_email",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("reference", "customer_email", "customer_phone")
    readonly_fields = ("reference", "created_at", "updated_at")


@admin.register(VoucherFile)
class VoucherFileAdmin(admin.ModelAdmin):
    list_display = ("uploaded_at", "processed", "error_message", "duration")
    readonly_fields = ("uploaded_at", "processed", "error_message")
    list_filter = ("duration",)
    actions = ["process_voucher_file"]

    def process_voucher_file(self, request, queryset):
        for voucher_file in queryset:
            if voucher_file.processed:
                self.message_user(
                    request,
                    f"File {voucher_file} has already been processed.",
                    level=messages.WARNING,
                )
                continue

            try:
                # Read and parse the CSV file
                with open(voucher_file.file.path, "r") as csvfile:
                    csv_reader = csv.DictReader(csvfile)

                    # Get the default duration
                    default_duration = voucher_file.duration

                    if not default_duration:
                        raise ValueError("No active voucher duration found")

                    # Create vouchers for each code
                    created_count = 0
                    for row in csv_reader:
                        code = row["Code"].strip()
                        # Check if voucher code already exists
                        if not Voucher.objects.filter(code=code).exists():
                            Voucher.objects.create(code=code, duration=default_duration)
                            created_count += 1

                voucher_file.processed = True
                voucher_file.save()

                self.message_user(
                    request,
                    f"Successfully processed {voucher_file}. Created {created_count} new vouchers.",
                    level=messages.SUCCESS,
                )

            except Exception as e:
                voucher_file.error_message = str(e)
                voucher_file.save()
                self.message_user(
                    request,
                    f"Error processing {voucher_file}: {str(e)}",
                    level=messages.ERROR,
                )

    process_voucher_file.short_description = "Process selected voucher files"
