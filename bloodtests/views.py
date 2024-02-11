from rest_framework import status, viewsets
from rest_framework.response import Response

from bloodtests.models import Test
from bloodtests.serializers import TestSerializer


class TestDetails(viewsets.ViewSet):
    def retrieve(self, request, **kwargs):
        code = kwargs.get("code").upper()

        try:
            blood_test = Test.objects.get(code=code)
        except Test.DoesNotExist:
            return Response(
                {"error": "Blood test not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TestSerializer(blood_test)
        return Response(serializer.data)

    def create(self, request, **kwargs):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            defaults = serializer.validated_data.copy()
            code = defaults.pop("code").upper()
            Test.objects.update_or_create(code=code, defaults=defaults)
            return Response(serializer.data, status=status.HTTP_200_OK)

        non_field_errors = serializer.errors.get("non_field_errors", [])
        if non_field_errors:
            return Response(non_field_errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
