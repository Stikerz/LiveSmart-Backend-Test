import pytest
from rest_framework.exceptions import ValidationError
from bloodtests.serializers import TestSerializer


@pytest.mark.django_db
class TestTestSerializer:

    @pytest.mark.parametrize(
        "field_name, invalid_value, error_message",
        [
            ("code", "ABCDE", "Ensure this field has no more than 4 characters."),
            ("name", "A" * 101, "Ensure this field has no more than 100 characters."),
            ("unit", "A" * 11, "Ensure this field has no more than 10 characters."),
        ],
    )
    def test_validate_field_length(
        self, valid_data, field_name, invalid_value, error_message
    ):
        valid_data[field_name] = invalid_value
        serializer = TestSerializer(data=valid_data)
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert error_message in str(excinfo.value)

    @pytest.mark.parametrize(
        "lower, upper, error_message",
        [
            (100, 50, "Lower value can't exceed upper value"),
            (None, None, "Lower and upper cannot both be null"),
        ],
    )
    def test_validate_lower_upper(self, valid_data, lower, upper, error_message):
        valid_data["lower"] = lower
        valid_data["upper"] = upper
        serializer = TestSerializer(data=valid_data)
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert error_message in str(excinfo.value)

    @pytest.mark.parametrize(
        "lower, expected_value",
        [
            (50, 50),
            (-50, None),
        ],
    )
    def test_validate_lower_positive(self, valid_data, lower, expected_value):
        valid_data["lower"] = lower
        serializer = TestSerializer(data=valid_data)
        if lower >= 0:
            assert serializer.is_valid()
            assert serializer.validated_data["lower"] == expected_value
        else:
            with pytest.raises(ValidationError) as excinfo:
                serializer.is_valid(raise_exception=True)
            assert "Lower value must be positive." in str(excinfo.value)

    @pytest.mark.parametrize(
        "upper, expected_value, error_message",
        [
            (200, 200, None),
            (-100, None, "Upper value must be positive."),
        ],
    )
    def test_validate_upper_positive(
        self, valid_data, upper, expected_value, error_message
    ):
        valid_data["upper"] = upper
        serializer = TestSerializer(data=valid_data)
        if upper >= 0:
            assert serializer.is_valid()
            assert serializer.validated_data["upper"] == expected_value
        else:
            with pytest.raises(ValidationError) as excinfo:
                serializer.is_valid(raise_exception=True)
            assert error_message in str(excinfo.value)

    @pytest.mark.parametrize("field_name", ["code", "name", "unit"])
    def test_validate_field_required(self, valid_data, field_name):
        valid_data.pop(field_name)
        serializer = TestSerializer(data=valid_data)
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert field_name in str(excinfo.value)
