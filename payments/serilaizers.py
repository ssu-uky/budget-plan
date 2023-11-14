from rest_framework import serializers
from rest_framework.exceptions import ValidationError, ParseError

from .models import Payment


class PaymentsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        models = Payment
        fields = [
            "owner",
            "pay_type",
            "pay_title",
            "pay_content",
            "pay_price",
            "pay_date",
        ]
