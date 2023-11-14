from django.db import models


class Payment(models.Model):
    class PayChoices(models.TextChoices):
        FOOD = "Food", "식비"
        CAFE = "Cafe", "카페"
        CLOTHES = "Clothes", "의류"
        PHONE = "Phone", "통신비"
        TRANSPORT = "Transport", "교통비"
        TRAVEL = "Travel", "여행"
        CULTURE = "Culture", "문화"
        HEALTH = "Health", "건강"
        BEAUTY = "Beauty", "미용"
        EDUCATION = "Education", "교육"
        PRESENT = "Present", "선물"
        ETC = "Etc", "기타"

    owner = models.ForeignKey(
        "users.User",
        related_name="payments",
        on_delete=models.CASCADE,
        blank=False,
    )

    pay_type = models.CharField(
        max_length=15,
        choices=PayChoices.choices,
        default=PayChoices.ETC,
    )

    pay_title = models.CharField(
        max_length=50,
        blank=False,
    )

    pay_content = models.TextField(
        max_length=200,
        blank=True,
    )

    pay_price = models.PositiveIntegerField(
        blank=False,
    )

    pay_date = models.DateTimeField(
        blank=False,
    )

    def __str__(self):
        return self.pay_title
