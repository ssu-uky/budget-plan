from django.urls import path
from . import views


urlpatterns = [
    path("monthly/", views.MonthlyPlanView.as_view(), name="monthly-plan"),
    path("daily/", views.DailyPlanView.as_view(), name="daily-plan"),
    path(
        "daily/<str:owner>/<int:year>-<int:month>-<int:day>/",
        views.DailyPlanDateView.as_view(),
        name="date-plan",
    ),
]
