"""
Django settings for demoproject project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import datetime

# Celery
# CELERY_BROKER_URL = '%s://%s:%s@%s:%s' % (os.environ.get('RABBITMQ_PROTOCOL'), os.environ.get('RABBITMQ_DEFAULT_USER'), os.environ.get(
#     'RABBITMQ_DEFAULT_PASS'), os.environ.get('RABBITMQ_HOST'), os.environ.get('RABBITMQ_PORT'))  # using rabbitmq
CELERY_BROKER_URL = "redis://%s:%s/0" % (
    os.environ.get("REDIS_CACHING_HOST"),
    os.environ.get("REDIS_CACHING_PORT"),
)  # using redis
CELERY_RESULT_BACKEND = f"redis://{os.environ.get('REDIS_CACHING_HOST')}:{os.environ.get('REDIS_CACHING_PORT')}/0"
CELERY_TASK_TRACK_STARTED = True
CELERY_RESULT_EXTENDED = True

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("ENVIRONMENT", "development") == "development"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "hoangdt.dev.icts.vn"]


# Application definition
INSTALLED_APPS = [
    "jazzmin",
    "keywordrecognition.apps.KeywordrecognitionConfig",
    "backend.apps.BackendConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third parties
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "main/templates"),
            os.path.join(BASE_DIR, "keywordrecognition/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "main.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_EXPOSE_PORT"),
    }
}

AUTH_USER_MODEL = "backend.Account"

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "vi"

LANGUAGES = (
    ("vi", "Vietnamese"),
    ("en", "English"),
)
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]


TIME_ZONE = "Asia/Ho_Chi_Minh"

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SESSION_COOKIE_SECURE = False

JWT_AUTH = {
    "JWT_ALGORITHM": "HS256",
    "JWT_EXPIRATION_DELTA": datetime.timedelta(seconds=30 * 60),
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(seconds=60 * 24 * 60 * 60),
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = ["https://hoangdt.dev.icts.vn"]

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
FIREBASE_PRIVATE_KEY_ID = os.environ.get("FIREBASE_PRIVATE_KEY_ID")
FIREBASE_PRIVATE_KEY = os.environ.get("FIREBASE_PRIVATE_KEY")
FIREBASE_CLIENT_EMAIL = os.environ.get("FIREBASE_CLIENT_EMAIL")
FIREBASE_CLIENT_ID = os.environ.get("FIREBASE_CLIENT_ID")
FIREBASE_CLIENT_CERT_URL = os.environ.get("FIREBASE_CLIENT_CERT_URL")

# drf-spectacular set up
REST_FRAMEWORK = {
    # YOUR SETTINGS
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Mytempura API",
    "DESCRIPTION": "This is a Mytempura official API documentation.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# FILE_UPLOAD_HANDLERS = [
#     'django.core.files.uploadhandler.TemporaryFileUploadHandler',
# ]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "keywordrecognition/static"),
]

JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": "MyTempura",
    # Title on the brand, and the login screen (19 chars max)
    "site_header": "MyTempura",
    "site_brand": "MyTempura",
    # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    "site_logo": "images/tempura-sumikko.jpg",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to MyTempura",
    # Copyright on the footer
    "copyright": "MyTempura",
    # The model admin to search from the search bar, search bar omitted if excluded
    # 'search_model': 'auth.User',
    # Field name on user model that contains avatar image
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        # external url that opens in a new window (Permissions can be added)
        {
            "name": "Support",
            "url": "https://github.com/tomodachii/mytempura/issues",
            "new_window": True,
        },
        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},
        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "polls"},
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ('app' url type is not allowed)
    # 'usermenu_links': [
    #     {'name': 'Support', 'url': 'https://github.com/farridav/django-jazzmin/issues', 'new_window': True},
    #     {'model': 'auth.user'}
    # ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps to base side menu ordering off of (does not need to contain all apps)
    "order_with_respect_to": [
        "auth",
        "backend",
        "keywordrecognition",
        "keywordrecognition.elizabot",
        "keywordrecognition.defaultmessage",
        "keywordrecognition.keyword",
        "keywordrecognition.decomp",
        "keywordrecognition.reasmb",
        "keywordrecognition.quit",
        "keywordrecognition.synonym",
        "keywordrecognition.postprocessing",
    ],
    # Custom links to append to app groups, keyed on app name
    # 'custom_links': {
    #     'backend': [{
    #         'name': 'Point Of Sale',
    #         'url': 'admin:point-of-sale',
    #         'icon': 'fas fa-cart-arrow-down',
    #     }]
    # },
    # Custom icons for side menu apps/models See https://www.fontawesomecheatsheet.com/font-awesome-cheatsheet-5x/
    # for a list of icon classes
    "icons": {
        "auth.Group": "fas fa-users",
        "backend.account": "fas fa-users-cog",
        "keywordrecognition.keyword": "fas fa-key",
        "keywordrecognition.elizabot": "fas fa-robot",
        "keywordrecognition.reasmb": "fas fa-recycle",
        "keywordrecognition.decomp": "fas fa-puzzle-piece",
        "keywordrecognition.defaultmessage": "fas fa-reply",
        "keywordrecognition.postprocessing": "fas fa-flag",
        "keywordrecognition.quit": "fas fa-stop",
        "keywordrecognition.synonym": "fas fa-equals",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    "language_chooser": True,
    # "related_modal_active": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-info",
    "accent": "accent-info",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-light-info",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "united",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

# changed in django 3.0 to DENY (affect add modal on admin)
# https://docs.djangoproject.com/en/3.1/ref/clickjacking/#setting-x-frame-options-for-all-responses
X_FRAME_OPTIONS = "SAMEORIGIN"

BACKEND_URL = os.environ.get("BACKEND_URL")
