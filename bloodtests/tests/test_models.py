import pytest
from django.db.utils import IntegrityError

from bloodtests.models import Test


@pytest.mark.django_db
class TestTestModel:

    @staticmethod
    def create_test_instance(**kwargs):
        defaults = {
            "code": "TEST",
            "name": "Test Name",
            "unit": "test/unit",
            "upper": 100,
            "lower": 50,
        }
        defaults.update(kwargs)
        return Test.objects.create(**defaults)

    def test_create_test_instance(self):
        test = self.create_test_instance()
        assert test.code == "TEST"
        assert test.name == "Test Name"
        assert test.unit == "test/unit"
        assert test.upper == 100
        assert test.lower == 50

    @pytest.mark.parametrize(
        "upper, lower",
        [
            (50, 100),
            (None, None),
        ],
    )
    def test_constraints(self, upper, lower):
        with pytest.raises(IntegrityError):
            self.create_test_instance(upper=upper, lower=lower)

    @pytest.mark.parametrize(
        "lower, upper, expected_ideal_range",
        [
            (50, 100, "50 <= value <= 100"),
            (50, None, "value >= 50"),
            (None, 100, "value <= 100"),
        ],
    )
    def test_ideal_range_property(self, lower, upper, expected_ideal_range):
        test_instance = self.create_test_instance(upper=upper, lower=lower)
        assert test_instance.ideal_range == expected_ideal_range
