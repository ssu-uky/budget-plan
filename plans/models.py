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

    # 한달 지출 목록
    monthly_spending = models.ManyToManyField(
        Payment,
        related_name="monthly_budgetplans",
        blank=True,
    )

    # 한달 총 지출 금액
    monthly_total_spending = models.PositiveIntegerField(
        default=0,
    )
    
    # 일일 예상 지출 금액
    today_plan = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    # 일일 지출 목록
    today_spending = models.ManyToManyField(
        Payment,
        related_name="daily_budgetplans",
        blank=True,
    )

    # 일일 총 지출 금액
    today_total_spending = models.PositiveIntegerField(
        default=0,
    )

    def __str__(self):
        return self.owner.username


class Notification(models.Model):
    """
    signal로 사용 할 알림 모델
    """

    receiver = models.ForeignKey(
        User,
        related_name="notifications",
        on_delete=models.CASCADE,
        blank=False,
    )
    title = models.CharField(
        max_length=100,
        blank=False,
    )
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receiver.username} - {self.title}"