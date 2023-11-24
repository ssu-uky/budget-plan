from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError

from .models import Payment
from .serializers import PaymentSerializer, DailyPaymentSerializer

from users.models import User


class PaymentListView(APIView):
    """
    GET : 지출 조회
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, owner):
        try:
            user = User.objects.get(username=owner)
            payments = Payment.objects.filter(owner=user)
            serializer = PaymentSerializer(payments, many=True)
            if request.user.username != owner:
                raise PermissionDenied

            total_price = sum(payment.pay_price for payment in payments)

            return Response(
                {"total_price": total_price, "payments": serializer.data},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                {"message": "존재하지 않는 사용자입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CreatePaymentView(APIView):
    """
    POST : 일 별 지출 입력
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "message": "지출을 입력해주세요.",
                "pay_type": "지출 유형",
                "pay_title": "지출 제목",
                "pay_content": "지출 내용",
                "pay_price": "지출 금액",
                "pay_date": "지출 일자",
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            pay_type = serializer.validated_data.get("pay_type")
            pay_title = serializer.validated_data.get("pay_title")
            pay_content = serializer.validated_data.get("pay_content")
            pay_price = serializer.validated_data.get("pay_price")
            pay_date = serializer.validated_data.get(
                "pay_date", timezone.localtime().date()
            )

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
                    "payment_id": payment.id,
                    "pay_type": payment.pay_type,
                    "pay_title": payment.pay_title,
                    "pay_content": payment.pay_content,
                    "pay_price": payment.pay_price,
                    "pay_date": payment.pay_date,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DailyPaymentView(APIView):
    """
    GET : 일 별 지출 조회(날짜로 조회)
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, owner, year, month, day):
        if request.user.username != owner:
            raise PermissionDenied

        user = User.objects.get(username=owner)
        today = datetime.date(year, month, day)

        payments = Payment.objects.filter(owner=user, pay_date=today)
        serializer = DailyPaymentSerializer(payments, many=True)

        today_total_price = sum(payment.pay_price for payment in payments)

        return Response(
            {"today_total_price": today_total_price, "payments": serializer.data},
            status=status.HTTP_200_OK,
        )


class DailyPaymentDetailView(APIView):
    """
    GET : payment pk로 지출 하나씩 상세 조회
    PUT : 일 별 지출 수정
    DELETE : 일 별 지출 삭제
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, owner, payment_pk):
        user = get_object_or_404(User, username=owner)
        return get_object_or_404(Payment, owner=user, pk=payment_pk)

    def get(self, request, owner, payment_pk):
        if request.user.username != owner:
            raise PermissionDenied
        payment = self.get_object(owner, payment_pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, owner, payment_pk):
        try:
            payment = Payment.objects.get(pk=payment_pk, owner=request.user)
            serializer = PaymentSerializer(payment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "일 별 지출이 수정되었습니다.",
                        "payment_id": payment.id,
                        "pay_type": payment.pay_type,
                        "pay_title": payment.pay_title,
                        "pay_content": payment.pay_content,
                        "pay_price": payment.pay_price,
                        "pay_date": payment.pay_date,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        except Payment.DoesNotExist:
            return Response(
                {"message": "지출 내역이 존재하지않습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, owner, payment_pk):
        try:
            payment = Payment.objects.get(pk=payment_pk, owner=request.user)
            payment.delete()
            return Response({"message": "일 별 지출이 삭제되었습니다."}, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response(
                {"message": "지출 내역이 존재하지않습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
