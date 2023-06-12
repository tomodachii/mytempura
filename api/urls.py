from django.urls import path
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
    # bot
    path("bots", views.ElizaBotAPIView.as_view(), name="eliza-bot"),
    path("bots/<int:id>", views.ElizaBotDetailAPI.as_view(), name="eliza-bot-detail"),
    path(
        "bots/<int:id>/load",
        views.ElizaBotLoadTxtAPIView.as_view(),
        name="eliza-bot-load-data",
    ),
    path(
        "bots/<int:bot_id>/load/<str:task_id>/status",
        views.ElizaBotLoadTxtStatusAPIView.as_view(),
        name="eliza-bot-load-data-status",
    ),
    path(
        "bots/<int:id>/response",
        views.ElizaBotGenerateResponseAPIView.as_view(),
        name="eliza-bot-response",
    ),
    # bot-keyword
    path(
        "bots/<int:bot_id>/keywords",
        views.KeywordAPI.as_view(),
        name="eliza-bot-keyword",
    ),
    # keyword
    path("keywords", views.KeywordAPI.as_view(), name="eliza-bot-keyword-create"),
    path(
        "keywords/<int:id>",
        views.KeywordDetailAPI.as_view(),
        name="eliza-bot-keyword-detail",
    ),
    # decomp
    # reasmb
]
