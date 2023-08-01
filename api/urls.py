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
    path("elizabots", views.ElizaBotAPIView.as_view(), name="eliza-bot"),
    path(
        "elizabots/<int:id>", views.ElizaBotDetailAPI.as_view(), name="eliza-bot-detail"
    ),
    path(
        "elizabots/<int:id>/load",
        views.ElizaBotLoadTxtAPIView.as_view(),
        name="eliza-bot-load-data",
    ),
    path(
        "elizabots/<int:bot_id>/load/<str:task_id>/status",
        views.ElizaBotLoadTxtStatusAPIView.as_view(),
        name="eliza-bot-load-data-status",
    ),
    path(
        "elizabots/<int:id>/response",
        views.ElizaBotGenerateResponseAPIView.as_view(),
        name="eliza-bot-response",
    ),
    # bot-keyword
    path(
        "elizabots/<int:bot_id>/keywords",
        views.KeywordAPI.as_view(),
        name="eliza-bot-keyword",
    ),
    # keyword
    path(
        "elizabots/keywords",
        views.KeywordAPI.as_view(),
        name="eliza-bot-keyword-create",
    ),
    path(
        "elizabots/keywords/<int:id>",
        views.KeywordDetailAPI.as_view(),
        name="eliza-bot-keyword-detail",
    ),
    # decomp
    # reasmb
    path(
        "nlpbots/<int:bot_id>/entities/upload",
        views.EntityUploadCSVAPIView.as_view(),
        name="nlp-upload-entities",
    ),
    path(
        "nlpbots/<int:bot_id>/intents/upload",
        views.IntentUploadCSVAPIView.as_view(),
        name="nlp-upload-intents",
    ),
    path(
        "nlpbots/<int:bot_id>/responses/upload",
        views.ResponseUploadCSVAPIView.as_view(),
        name="nlp-upload-responses",
    ),
]
