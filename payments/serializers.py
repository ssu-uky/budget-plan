from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, ParseError

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Payment
        fields = [
            "owner",
            "pay_type",
            "pay_title",
            "pay_content",
            "pay_price",
            "pay_date",
        ]

        read_only_fields = ["owner"]
