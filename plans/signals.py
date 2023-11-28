from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.utils import timezone

from .models import BudgetPlan, Notification
from payments.models import Payment
from users.models import User


@receiver(post_save, sender=Payment)
@receiver(post_delete, sender=Payment)
def update_today_total_spending(sender, instance, **kwargs):
    today_date = timezone.localtime().date()
    today_payments = Payment.objects.filter(pay_date=today_date, owner=instance.owner)
    today_total_spending = sum(payment.pay_price for payment in today_payments)

    budget_plan, created = BudgetPlan.objects.get_or_create(owner=instance.owner)
    budget_plan.today_total_spending = today_total_spending
    budget_plan.save()

    # today_plan과 today_total_spending 비교
    if budget_plan.today_plan < today_total_spending:
        message = f"오늘의 사용 가능 금액은 {budget_plan.today_plan}원입니다. 현재 사용하신 금액은 {today_total_spending}원 입니다."
        Notification.objects.create(
            receiver=instance.owner, title="일일 지출 예산금액을 초과하였습니다.", message=message
        )
