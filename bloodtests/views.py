from rest_framework import status, viewsets
from rest_framework.response import Response

from bloodtests.models import Test
from bloodtests.serializers import TestSerializer


class TestDetails(viewsets.ViewSet):
    def retrieve(self, request, **kwargs):
        code = kwargs.get("code").upper()

        queryset = Test.objects.filter(code=code)
        if not queryset.exists():
            return Response(
                {"error": "Blood test not found"}, status=status.HTTP_404_NOT_FOUND
            )

        blood_test = queryset.first()
        serializer = TestSerializer(blood_test)
        return Response(serializer.data)

    def create(self, request, **kwargs):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            defaults = serializer.data.copy()
            code = defaults.pop("code")
            test_instance, created = Test.objects.get_or_create(
                code=code.upper(), defaults=defaults
            )
            if not created:
                test_instance.name = defaults.get("name")
                test_instance.unit = defaults.get("unit")
                test_instance.upper = defaults.get("upper")
                test_instance.lower = defaults.get("lower")
                test_instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        non_field_errors = serializer.errors.get("non_field_errors", [])
        if non_field_errors:
            return Response(non_field_errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
