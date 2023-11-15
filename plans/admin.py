from django.contrib import admin
from .models import BudgetPlan


@admin.register(BudgetPlan)
class BudgetPlanAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "monthly_income",
        "monthly_plan",
        "monthly_saving",
        "daily_plan",
    )
    list_display_links = ("owner",)
    search_fields = ("owner__username",)
    list_filter = ("owner",)
    filter_horizontal = ("daily_spending",)
    fieldsets = (
        (
            "BudgetPlan",
            {
                "fields": (
                    "owner",
                    "monthly_income",
                    "monthly_plan",
                    "monthly_saving",
                    "daily_spending",
                    "daily_plan",
                )
            },
        ),
    )
