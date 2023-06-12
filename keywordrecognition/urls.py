from django.urls import path

# from keywordrecognition import views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("swagger/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path(
        "swagger/redoc", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]
