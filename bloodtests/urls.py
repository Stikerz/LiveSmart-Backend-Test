from django.urls import path
from .views import TestDetails


urlpatterns = (
    path(
        "test/<str:code>",
        TestDetails.as_view({"get": "retrieve", "post": "create"}),
        name="api-bloodtests",
    ),
)
