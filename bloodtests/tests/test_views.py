import pytest
from django.urls import reverse
from bloodtests.serializers import TestSerializer
import json
from bloodtests.models import Test
from rest_framework import status


@pytest.mark.django_db
class TestTestDetails:

    @pytest.mark.parametrize(
        "code, expected_status",
        [("CHO", status.HTTP_200_OK), ("INVALID", status.HTTP_404_NOT_FOUND)],
    )
    def test_retrieve_test(self, api_client, code, expected_status, existing_test):
        response = api_client.get(reverse("api-bloodtests", kwargs={"code": code}))
        assert response.status_code == expected_status
        if code == "CHO":
            test_instance = Test.objects.get(code=code)
            assert response.data == TestSerializer(test_instance).data
        else:
            assert response.data == {"error": "Blood test not found"}

    @pytest.mark.parametrize(
        "data, expected_status",
        [
            (
                {
                    "code": "CHO",
                    "name": "Cholesterol",
                    "unit": "g/M",
                    "upper": 200,
                    "lower": 100,
                },
                status.HTTP_200_OK,
            ),
            ({"code": "CHO", "name": "Invalid Test"}, status.HTTP_400_BAD_REQUEST),
        ],
    )
    def test_create_test(self, api_client, data, expected_status):
        response = api_client.post(
            reverse("api-bloodtests", kwargs={"code": data.get("code")}),
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == expected_status
        if expected_status == status.HTTP_200_OK:
            assert Test.objects.filter(code=data["code"]).exists()
