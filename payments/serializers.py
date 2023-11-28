from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, ParseError

from .models import Payment
from plans.models import BudgetPlan


class PaymentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Payment
        fields = "__all__"

        read_only_fields = ["owner"]


class DailyPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "pay_type", "pay_title", "pay_content", "pay_price", "pay_date"


class BudgetPlanSerializer(serializers.Serializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    monthly_spending = PaymentSerializer(many=True, read_only=True)
    today_spending = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = BudgetPlan
        fields = [
            "owner",
            "monthly_income",
            "monthly_plan",
            "monthly_saving",
            "monthly_spending",
            "today_spending",
            "today_plan",
        ]
