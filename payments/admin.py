from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "pay_type",
        "pay_title",
        # "pay_content",
        "pay_price",
        "pay_date",
    )
    list_display_links = (
        "id",
        "owner",
        "pay_type",
        "pay_title",
    )

    ordering = ("-pay_date",)
