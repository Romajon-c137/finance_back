from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.account.views import Login
from apps.finance.views import (
    FinanceModelViewSet,
    ConsumptionModelViewSet,
    GetPerson,
    GetPersonCategory,
    GetTransactions,
    SalaryModelViewSet,
)

router = DefaultRouter()
router.register("finances", FinanceModelViewSet)
router.register("consumptions", ConsumptionModelViewSet)
router.register("salaries", SalaryModelViewSet)

urlpatterns = [
    path("auth/login/", Login.as_view(), name="auth-login"),
    # persons
    path("persons/",GetPerson.as_view(),name="persons"),
    path("persons/<str:category>/",GetPersonCategory.as_view(),name="persons"),
    path("persons/<int:person_id>/transactions/",GetTransactions.as_view(),name="persons"),
    #
    path("", include(router.urls)),
]
