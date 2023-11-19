from django.db import models

from users.models import User
from payments.models import Payment


class BudgetPlan(models.Model):
    """
    예산 계획 모델
    """

    owner = models.ForeignKey(
        User,
        related_name="budgetplans",
        on_delete=models.CASCADE,
        blank=False,
    )

    # 한달 수입 (monthly_income = monthly_plan + monthly_saving)
    monthly_income = models.PositiveIntegerField(
        blank=False,
    )

    # 한달 예상 지출 금액
    monthly_plan = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    # 한달 저축 금액
    monthly_saving = models.PositiveIntegerField(
        blank=False,
    )

    # 일일 지출 금액
    daily_spending = models.ManyToManyField(
        Payment,
        related_name="budgetplans",
        blank=True,
    )

    # 일일 예상 지출 금액
    daily_plan = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.owner.username
