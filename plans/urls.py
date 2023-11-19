from django.urls import path
from . import views


urlpatterns = [
    path("monthly/", views.MonthlyPlanView.as_view(), name="monthly_plan"),
]
