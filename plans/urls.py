from django.urls import path
from . import views


urlpatterns = [
    path("monthly-plan/", views.MonthlyPlanView.as_view(), name="monthly-plan"),
    # path("daily-plan/", views.DailyPlanView.as_view(), name="daily-plan"),
    # path("daily-plan/<int:year>-<int:month>-<int:day>/", views.DailyPlanView.as_view(), name="daily_plan"),
    path("daily-plan/<str:owner>/<int:year>-<int:month>-<int:day>/", views.DailyPlanView.as_view(), name="daily_plan"),
]
