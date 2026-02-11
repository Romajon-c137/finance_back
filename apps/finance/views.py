from rest_framework.views import APIView
from apps.finance.serializers import *
from utils.mixins import UltraModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.status import HTTP_201_CREATED
from rest_framework.generics import get_object_or_404
from drf_yasg import openapi
from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema
from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import action, permission_classes

from utils.paginations import PaginatorClass
from utils.permissions import ReturnFalse

from .models import *


class BaseAbstractModelViewSet(UltraModelViewSet):
    search_fields = ["name"]
    ordering_fields = ["create_dt"]
    permission_classes_by_action = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [ReturnFalse],
        "destroy": [ReturnFalse],
    }
    pagination_class = PaginatorClass

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(owner=user)

        return queryset


class FinanceModelViewSet(BaseAbstractModelViewSet):
    queryset = Finance.objects
    serializer_classes = {
        "list": ListFinanceSerializer,
        "retrieve": RetrieveFinanceSerializer,
        "create": CreateFinanceSerializer,
        "update": CreateFinanceSerializer,
    }


class ConsumptionModelViewSet(BaseAbstractModelViewSet):
    queryset = Consumption.objects
    serializer_classes = {
        "list": ListConsumptionSerializer,
        "retrieve": RetrieveConsumptionSerializer,
        "create": CreateConsumptionSerializer,
        "update": CreateConsumptionSerializer,
    }


class SalaryModelViewSet(BaseAbstractModelViewSet):
    queryset = Salary.objects
    serializer_classes = {
        "list": ListSalarySerializer,
        "retrieve": RetrieveSalarySerializer,
        "create": CreateSalarySerializer,
        "update": CreateSalarySerializer,
    }


class GetPerson(APIView):

    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        return Response(
            [
                {"finance": "Финансы"},
                {"consumption": "Расход"},
                {"salary": "Зарплата"},
            ]
        )

    @swagger_auto_schema(
        operation_description="Создание person записи",
        request_body=CreatePersonSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(
                        type=openapi.TYPE_STRING, example="success"
                    ),
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING, example="Финансовая запись создана"
                    ),
                    "finance_id": openapi.Schema(
                        type=openapi.TYPE_INTEGER, example=123
                    ),
                },
            )
        },
    )
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        owner = request.user
        data = request.data

        serializer = CreatePersonSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        class_type_FCM = ContentType.objects.get_for_model(
            CLASS_TYPE_FINANCE_CHOICES_MAPPING[serializer.validated_data["type_class"]]
        )

        res = Person.objects.create(
            name=serializer.validated_data["name"],
            content_type=class_type_FCM,
            owner=owner,
        )

        return Response(
            {
                "id": res.pk,
                **serializer.data,
            },
            status=HTTP_201_CREATED,
        )


class GetPersonCategory(APIView):
    pagination_class = PaginatorClass

    def get(self, request, category, *args, **kwargs):
        """Возвращает данные по категории"""

        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Вы не авторизованы"}, status=401)

        if category in CLASS_TYPE_FINANCE_CHOICES_MAPPING:

            res = CLASS_TYPE_FINANCE_CHOICES_MAPPING[category]

            class_type_FCM = ContentType.objects.get_for_model(res)

            res_person = Person.objects.filter(owner=user, content_type=class_type_FCM)

            paginator = self.pagination_class()
            page = paginator.paginate_queryset(res_person, request)

            serializer = PersonSerializer(page, many=True)

            return paginator.get_paginated_response(serializer.data)
        return Response({"error": "Категория не найдена"}, status=404)


class GetTransactions(APIView):
    pagination_class = PaginatorClass

    def get(self, request, person_id, *args, **kwargs):
        owner = request.user
        # Получаем Person
        person = get_object_or_404(Person, pk=person_id, owner=owner)

        search = request.query_params.get("search", None)
        print(search)

        # Класс модели через ContentType
        model_class = person.content_type.model_class()
        if not model_class:
            return Response({"detail": "Invalid content type"}, status=400)

        qs = model_class.objects.filter(person=person, owner=request.user)
        if search:
            qs = model_class.objects.filter(
                Q(person=person), Q(owner=request.user), Q(name__icontains=search)
            )

        # Пагинация
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)

        # Сериализация
        serializer_class = SERIALIZER_MAPPING.get(model_class)
        if not serializer_class:
            return Response(
                {"detail": "No serializer defined for this model"}, status=500
            )

        serializer = serializer_class(page, many=True)

        # Убираем поле "person"
        data = [
            {k: v for k, v in item.items() if k != "person"} for item in serializer.data
        ]

        return paginator.get_paginated_response(data)
