from django.db import models
from django.db.models import CheckConstraint, Q


class TestResult:
    pass


class Test(models.Model):
    """Laboratory tests information"""

    code = models.CharField(max_length=4)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)
    upper = models.FloatField(null=True, blank=True)
    lower = models.FloatField(null=True, blank=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(lower__isnull=False) | Q(upper__isnull=False),
                name="lower_or_upper_not_both_null",
            ),
            CheckConstraint(
                check=models.Q(upper__gt=models.F("lower")),
                name="upper_greater_than_lower",
            ),
        ]

    @property
    def ideal_range(self):
        if self.lower is not None and self.upper is not None:
            return f"{self.lower} <= value <= {self.upper}"
        elif self.lower is not None:
            return f"value >= {self.lower}"
        elif self.upper is not None:
            return f"value <= {self.upper}"
