from django.contrib import admin
from .models import VoucherDuration, Voucher, Transaction


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
