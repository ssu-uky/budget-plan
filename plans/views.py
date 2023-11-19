from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from .models import BudgetPlan
from .serializers import MonthlyPlanSerializer


class MonthlyPlanView(APIView):
    """
    POST : 한 달 예산 계획
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # return Response({"message": "예산 계획을 입력해주세요."})
        return Response(
            {
                "message": "예산 계획을 입력해주세요.",
                "monthly_income": "한달 수입 금액",
                "monthly_saving": "한달 저축 금액",
            }
        )

    def post(self, request):
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
