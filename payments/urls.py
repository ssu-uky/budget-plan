from django.urls import path
from . import views


urlpatterns = [
    path("daily/", views.CreatePaymentView.as_view(), name="payment"),
    path("<str:owner>/", views.PaymentListView.as_view(), name="payment-list"),
    path(
        "<str:owner>/<int:year>-<int:month>-<int:day>/",
        views.DailyPaymentView.as_view(),
        name="payment-list",
    ),
    path(
        "<str:owner>/<int:payment_pk>",
        views.DailyPaymentDetailView.as_view(),
        name="payment-detail",
    ),
]
