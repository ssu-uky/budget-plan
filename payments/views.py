from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from .models import Payment
from .serializers import PaymentSerializer


class DailyPaymentView(APIView):
    """
    GET : 일 별 지출 조회
    POST : 일 별 지출 입력
    PUT : 일 별 지출 수정
    DELETE : 일 별 지출 삭제
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "message": "일 별 지출을 입력해주세요.",
                "pay_type": "지출 유형",
                "pay_title": "지출 제목",
                "pay_content": "지출 내용",
                "pay_price": "지출 금액",
                "pay_date": "지출 날짜",
            }
        )

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            pay_type = serializer.validated_data.get("pay_type")
            pay_title = serializer.validated_data.get("pay_title")
            pay_content = serializer.validated_data.get("pay_content")
            pay_price = serializer.validated_data.get("pay_price")
            pay_date = serializer.validated_data.get("pay_date")

            payment = Payment(
                owner=request.user,
                pay_type=pay_type,
                pay_title=pay_title,
                pay_content=pay_content,
                pay_price=pay_price,
                pay_date=pay_date,
            )
            payment.save()

            return Response(
                {
                    "message": "일 별 지출이 저장되었습니다.",
                    "pay_type": payment.pay_type,
                    "pay_title": payment.pay_title,
                    "pay_content": payment.pay_content,
                    "pay_price": payment.pay_price,
                    "pay_date": payment.pay_date,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
