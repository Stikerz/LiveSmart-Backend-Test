import pytest
from bloodtests.models import Test
from rest_framework.test import APIClient


@pytest.fixture
def valid_data():
    return {
        "code": "CHO",
        "name": "Cholesterol",
        "unit": "test/uni",
        "upper": 200,
        "lower": 100,
    }


@pytest.fixture
def invalid_test_data():
    return {
        "code": "ABC",
        "name": "Test Name",
        "unit": "test/uni",
        "upper": 100,
        "lower": 200,  # Invalid lower value
    }


@pytest.fixture
def existing_test(valid_data):
    return Test.objects.create(**valid_data)


@pytest.fixture
def api_client():
    return APIClient()
