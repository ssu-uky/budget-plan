from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import BudgetPlan


class MonthlyPlanSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    monthly_plan = serializers.SerializerMethodField()

    class Meta:
        model = BudgetPlan
        fields = [
            "owner",
            "monthly_income",
            "monthly_saving",
            "monthly_plan",
        ]

    def get_monthly_plan(self, obj):
        return obj.monthly_income - obj.monthly_saving

    read_only_fields = ["owner"]
    
    def validate(self, data):
        if data.get("monthly_saving") > data.get("monthly_income"):
            raise ValidationError("월 저축금액은 월 수입보다 클 수 없습니다.")
        return data


class BudgetPlanSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    monthly_plan = serializers.SerializerMethodField()
    daily_spending = serializers.ReadOnlyField(source="daily_spending.pay_price")
    daily_plan = serializers.ReadOnlyField(source="daily_plan")

    class Meta:
        model = BudgetPlan
        fields = [
            "owner",
            "monthly_income",
            "monthly_plan",
            "monthly_saving",
            "daily_spending",
            "daily_plan",
        ]

    def get_monthly_income(self, obj):
        return obj.monthly_plan + obj.monthly_saving

    def get_monthly_plan(self, obj):
        return obj.monthly_income - obj.monthly_saving
    
