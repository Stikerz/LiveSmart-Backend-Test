from django.contrib import admin

from bloodtests.models import Test, TestResult


class TestAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "unit", "upper", "lower", "ideal_range")
    search_fields = ("code", "name")
    list_filter = ("unit",)
    readonly_fields = ("ideal_range",)


admin.site.register(Test)
# admin.site.register(TestResult)
