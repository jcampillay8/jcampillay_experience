import os
from pathlib import Path
from django.contrib.messages import constants as messages
import dj_database_url
from dotenv import load_dotenv
import json
import dj_database_url
import environ

# Inicializa la carga de entorno
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

# Lista de hosts permitidos
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['0.0.0.0', '*', 'localhost', '127.0.0.1', 'web-production-299a1.up.railway.app'])

# Otras configuraciones
CSRF_TRUSTED_ORIGINS = ['http://*', 'https://web-production-299a1.up.railway.app']


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'whitenoise.runserver_nostatic',
]

PROJECT_APPS = [
    'apps.authentication',
    'apps.home',
    'apps.about_me',
    'apps.technical_insight',
    'apps.contact',
    'apps.Error_handler',
    'apps.blog',
    'apps.Quizzes',
]

THIRD_PARTY_APPS = [
    'livereload',
    'guest_user',
    'six',
    'widget_tweaks',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'django_bootstrap_icons',
    'bootstrap4',
    'dpd_static_support',
    
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

HANDLER404 = 'apps.Error_Handler.views.Error404View'
HANDLER500 = 'apps.Error_Handler.views.Error505View'

SESSION_SAVE_EVERY_REQUEST = True

with open('language.json', 'r', encoding='utf-8') as file:
    LANGUAGE_DATA = json.load(file)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'livereload.middleware.LiveReloadScript',
    'core.languagemiddleware.LanguageMiddleware',
    'django_plotly_dash.middleware.BaseMiddleware',
    'django_plotly_dash.middleware.ExternalRedirectionMiddleware',
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR/ 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.context_processors.language_code",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': env('DB_NAME'),
#         'USER': env('DB_USER'),
#         'PASSWORD': env('DB_PASSWORD'),
#         'HOST': env('DB_HOST'),
#         'PORT': env('DB_PORT'),
#     }
# }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

AUTHENTICATION_BACKENDS = [
    # ...
    'django.contrib.auth.backends.ModelBackend',
    'guest_user.backends.GuestBackend',
    # ...
]



LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English')
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
    'django_plotly_dash.finders.DashAppDirectoryFinder',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'


STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STATIC_URL = '/assets/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/assets')
]

STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


PLOTLY_DASH = {

    # Route used for the message pipe websocket connection
    "ws_route" :   "dpd/ws/channel",

    # Route used for direct http insertion of pipe messages
    "http_route" : "dpd/views",

    # Flag controlling existince of http poke endpoint
    "http_poke_enabled" : True,

    # Insert data for the demo when migrating
    "insert_demo_migrations" : False,

    # Timeout for caching of initial arguments in seconds
    "cache_timeout_initial_arguments": 60,

    # Name of view wrapping function
    "view_decorator": None,

    # Flag to control location of initial argument storage
    "cache_arguments": True,

    # Flag controlling local serving of assets
    "serve_locally": False,
    # Name of view wrapping function
    "view_decorator": "django_plotly_dash.access.login_required",
}

PLOTLY_COMPONENTS = [
    # core components required for use of most plotly dash components
    'dash_core_components',
    'dash_html_components',
    'dash_renderer',
    'dash_bootstrap_components',
    # django-plotly-dash components
    'dpd_components',
    'dpd_static_support',
]

MESSAGE_TAGS = {    
    messages.ERROR: 'danger'
}

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

X_FRAME_OPTIONS = 'SAMEORIGIN'
CSRF_COOKIE_NAME = 'csrftoken'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'welcome'