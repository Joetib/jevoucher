from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path("", views.VoucherDurationListView.as_view(), name="voucher_list"),
    path(
        "payment/initiate/",
        views.InitiatePaymentView.as_view(),
        name="initiate_payment",
    ),
    path(
        "payment/verify/<uuid:reference>/",
        views.VerifyPaymentView.as_view(),
        name="verify_payment",
    ),
]
