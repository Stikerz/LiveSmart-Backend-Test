from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bloodtests.models import Test


class TestSerializer(serializers.ModelSerializer):
    ideal_range = serializers.ReadOnlyField()

    class Meta:
        model = Test
        fields = ["code", "name", "unit", "upper", "lower", "ideal_range"]

    def validate_lower(self, value):
        if value is not None and value < 0:
            raise ValidationError("Lower value must be positive.")
        return value

    def validate_upper(self, value):
        if value is not None and value < 0:
            raise ValidationError("Upper value must be positive.")
        return value

    def validate(self, data):
        lower = data.get("lower")
        upper = data.get("upper")

        if lower is None and upper is None:
            raise ValidationError("Lower and upper cannot both be null")

        if lower is not None and upper is not None:
            if lower >= upper:
                raise ValidationError("Lower value can't exceed upper value")

        return data
