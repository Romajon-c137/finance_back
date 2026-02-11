from rest_framework import serializers

from utils.models import BaseFinance

from .models import (
    Person,
    Consumption,
    Salary,
    Finance,
    CLASS_TYPE_FINANCE_CHOICES_MAPPING,
)


class CreateAbstractSerializer(serializers.ModelSerializer):

    class Meta:
        abstract = True

    def create(self, validated_data):
        request = self.context.get("request")

        if not hasattr(request, "user"):
            raise serializers.ValidationError({"user": "Нет пользователя"})

        validated_data["owner"] = request.user

        return super().create(validated_data)


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = (
            "id",
            "name",
            "total_sum",
            "content_type",
        )


class ListFinanceSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = Finance
        fields = (
            "id",
            "name",
            "cash",
            "type_finance",
            "return_cash",
            "owner",
            "person",
            "create_dt",
        )


class RetrieveFinanceSerializer(ListFinanceSerializer):
    pass


class CreateFinanceSerializer(CreateAbstractSerializer):

    class Meta:
        model = Finance
        fields = (
            "cash",
            "name",
            "person",
            "type_finance",
            "return_cash",
        )


class ListConsumptionSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = Consumption
        fields = (
            "id",
            "name",
            "cash",
            "person",
        )


class RetrieveConsumptionSerializer(ListConsumptionSerializer):
    pass


class CreateConsumptionSerializer(CreateAbstractSerializer):

    class Meta:
        model = Consumption
        fields = (
            "name",
            "cash",
            "person",
        )


class ListSalarySerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = Salary
        fields = (
            "id",
            "cash",
            "person",
        )


class RetrieveSalarySerializer(ListSalarySerializer):
    pass


class CreateSalarySerializer(CreateAbstractSerializer):

    class Meta:
        model = Salary
        fields = (
            "name",
            "cash",
            "person",
        )


class CreatePersonSerializer(serializers.Serializer):
    name = serializers.CharField()
    type_class = serializers.CharField()

    def validate_type_class(self, value):

        if value not in CLASS_TYPE_FINANCE_CHOICES_MAPPING:
            raise serializers.ValidationError("Неверный тип операции")
        return value


SERIALIZER_MAPPING = {
    Finance: ListFinanceSerializer,
    Salary: ListSalarySerializer,
    Consumption: ListConsumptionSerializer,
}
