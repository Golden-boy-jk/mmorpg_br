from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-4=9qfug4h16)c_grbooh=mr*a6(1w#)rwful&9ugn0t%cvsd$r"
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
AUTH_USER_MODEL = "users.CustomUser"

SITE_ID = 1

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "board",
    "newsletter.apps.NewsletterConfig",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.yandex",
    "django_celery_beat",
    "django.contrib.flatpages",
    "django_filters",
    "django_ckeditor_5",
    "ckeditor_uploader",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "fan_mmorpg_board.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates" / "email" / "confirmation_email.html"],
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

WSGI_APPLICATION = "fan_mmorpg_board.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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


LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

SOCIALACCOUNT_PROVIDERS = {
    "yandex": {
        "APP": {
            "client_id": "df62cfc8ca154be9b0c1f62250cfdec1",
            "secret": "e261f3d79fe24bc2b3c735d5c1cd6e1d",
        },
        "SCOPE": ["login:email"],
        "AUTH_PARAMS": {"force_confirm": "yes"},
    }
}

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SOCIAL_AUTH_ASSOCIATE_BY_EMAIL = True

ACCOUNT_LOGOUT_REDIRECT_URL = "/"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.yandex.ru"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "dotan-games@yandex.ru"
EMAIL_HOST_PASSWORD = "lrtftilbvubbzybk"
DEFAULT_FROM_EMAIL = "dotan-games@yandex.ru"
SERVER_EMAIL = EMAIL_HOST_USER
SITE_URL = "http://127.0.0.1:8000"

LOGIN_REDIRECT_URL = "/users/home/"
LOGIN_URL = "ads/my_ads/"
LOGOUT_REDIRECT_URL = "/users/login/"

CELERY_BROKER_URL = "redis://default:Lon2DuGEPn3ZLVwUOrm2qtUrY9xRDYsA@redis-13805.c135.eu-central-1-1.ec2.redns.redis-cloud.com:13805"
CELERY_RESULT_BACKEND = "redis://default:Lon2DuGEPn3ZLVwUOrm2qtUrY9xRDYsA@redis-13805.c135.eu-central-1-1.ec2.redns.redis-cloud.com:13805"
# CELERY_TASK_ALWAYS_EAGER = True
# CELERY_BROKER_USE_SSL = True
# CELERY_RESULT_BACKEND_USE_SSL = True
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_5_CONFIGS = {
    'extends': {
        'language': 'ru',
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'link', 'underline', 'strikethrough', '|',
            'bulletedList', 'numberedList', '|',
            'blockQuote', 'codeBlock', '|',
            'insertTable', 'mediaEmbed', '|',
            'undo', 'redo'
        ],
    },
    'simple': {
        'language': 'en',
        'toolbar': ['bold', 'italic', 'link']
    }
}

