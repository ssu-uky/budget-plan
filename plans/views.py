import calendar
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError

from .models import BudgetPlan
from .serializers import MonthlyPlanSerializer

from payments.models import Payment
from users.models import User


class MonthlyPlanView(APIView):
    """
    POST : 한 달 예산 계획 입력
    PUT : 한 달 예산 계획 수정
    DELETE : 한 달 예산 계획 삭제
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "message": "예산 계획을 입력해주세요.",
                "monthly_income": "한달 수입 금액",
                "monthly_saving": "한달 저축 금액",
            }
        )

    def post(self, request):
        exist_plan = BudgetPlan.objects.filter(owner=request.user).exists()
        if exist_plan:
            return Response(
                {"message": "이미 예산 계획이 있습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = MonthlyPlanSerializer(data=request.data)
        if serializer.is_valid():
            monthly_income = serializer.validated_data.get("monthly_income")
            monthly_saving = serializer.validated_data.get("monthly_saving")
            monthly_plan = monthly_income - monthly_saving

            budget_plan = BudgetPlan(
                owner=request.user,
                monthly_income=monthly_income,
                monthly_saving=monthly_saving,
                monthly_plan=monthly_plan,
            )
            budget_plan.save()

            return Response(
                {
                    "message": "예산 계획이 저장되었습니다.",
                    "monthly_income": budget_plan.monthly_income,
                    "monthly_saving": budget_plan.monthly_saving,
                    "monthly_plan": budget_plan.monthly_plan,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            budget_plan = BudgetPlan.objects.get(owner=request.user)
            serializer = MonthlyPlanSerializer(data=request.data)
            if serializer.is_valid():
                monthly_income = serializer.validated_data.get("monthly_income")
                monthly_saving = serializer.validated_data.get("monthly_saving")
                monthly_plan = monthly_income - monthly_saving

                budget_plan.monthly_income = monthly_income
                budget_plan.monthly_saving = monthly_saving
                budget_plan.monthly_plan = monthly_plan
                budget_plan.save()

                return Response(
                    {
                        "message": "예산 계획이 수정되었습니다.",
                        "monthly_income": budget_plan.monthly_income,
                        "monthly_saving": budget_plan.monthly_saving,
                        "monthly_plan": budget_plan.monthly_plan,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BudgetPlan.DoesNotExist:
            return Response(
                {"message": "예산 계획이 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request):
        try:
            budget_plan = BudgetPlan.objects.get(owner=request.user)
            budget_plan.delete()
            return Response({"message": "예산 계획이 삭제되었습니다."}, status=status.HTTP_200_OK)
        except BudgetPlan.DoesNotExist:
            return Response(
                {"message": "예산 계획이 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )


class DailyPlanView(APIView):
    """
    GET : 일일 지출 현황 조회 (날짜로 조회)
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, owner, year, month, day):
        user = get_object_or_404(User, username=owner)
        return get_object_or_404(
            Payment,
            owner=user,
            pay_date__year=year,
            pay_date__month=month,
            pay_date__day=day,
        )

    def get(self, request, owner, year=None, month=None, day=None):
        if request.user.username != owner:
            raise PermissionDenied
        try:
            budget_plan = BudgetPlan.objects.get(owner=request.user)
            
            if year and month and day:
                try:
                    today_date = timezone.datetime(year, month, day).date()
                except ValueError:
                    return Response(
                        {"message": "해당 일을 조회할 수 없습니다."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                today_date = timezone.now().date()

            # if year and month and day:
            #     today_date = timezone.datetime(year, month, day).date()
            # else:
            #     today_date = timezone.now().date()

            # 해당 월의 총 일수와 현재 날짜 구하기
            _, last_day_of_month = calendar.monthrange(
                today_date.year, today_date.month
            )
            current_day = today_date.day

            # 현재 월에 대한 지출 합계 구하기
            monthly_payments = Payment.objects.filter(
                owner=request.user,
                pay_date__year=today_date.year,
                pay_date__month=today_date.month,
            )
            total_monthly_spending = sum(
                payment.pay_price for payment in monthly_payments
            )

            # 오늘까지의 일일 평균 예산 계산
            remaining_days = last_day_of_month - current_day + 1

            daily_plan = (
                budget_plan.monthly_plan - total_monthly_spending
            ) / remaining_days
            # 100원 단위로 반올림
            daily_plan = round(daily_plan / 100) * 100

            # 음수일 경우 0으로 처리
            # daily_plan = max(daily_plan, 0)

            # 오늘의 지출 내역
            daily_payments = Payment.objects.filter(
                owner=request.user, pay_date=today_date
            )
            today_spending = [
                {
                    # "type": payment.pay_type,
                    "title": payment.pay_title,
                    # "content": payment.pay_content,
                    "price": payment.pay_price,
                    # "date": payment.pay_date,
                }
                for payment in daily_payments
            ]
            today_total_spending = sum(payment.pay_price for payment in daily_payments)

            data = {
                # "monthly_plan": budget_plan.monthly_plan,
                "daily_plan": daily_plan,
                "monthly_amounts": total_monthly_spending,
                "today_spending": today_spending,
                "today_total_spending": today_total_spending,
            }

            return Response(data, status=status.HTTP_200_OK)
        except BudgetPlan.DoesNotExist:
            return Response(
                {"message": "예산 계획이 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )
