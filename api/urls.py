from django.urls import include, path
from api import views
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
    path("auth/sign-up", views.SignUpAPIView.as_view(), name="sign-up"),
    path("auth/sign-in", views.SignInAPIView.as_view(), name="sign-in"),
    # keyword-recognition
    path("keywordrecognition/", include("keywordrecognition.urls")),
]
