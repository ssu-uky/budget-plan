from django.urls import path
from . import views


urlpatterns = [
    path("daily/", views.DailyPaymentView.as_view(), name="daily-pay"),
]
