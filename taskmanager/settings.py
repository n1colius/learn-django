"""
Django settings for taskmanager project.

=== LARAVEL COMPARISON ===
This file is like Laravel's .env + config/ folder combined.
- Laravel: config/database.php, config/app.php, .env
- Django:  settings.py (one file holds it all)
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Same as Laravel's base_path() helper
BASE_DIR = Path(__file__).resolve().parent.parent

# Like Laravel's APP_KEY in .env
SECRET_KEY = 'django-insecure-5$_o3mnis^04at4q98ii%yayia*f4-2$u1$@m9grc_gxz*z%2d'

# Like Laravel's APP_DEBUG in .env
DEBUG = True

ALLOWED_HOSTS = []


# ============================================================
# INSTALLED_APPS = Like Laravel's config/app.php 'providers' array
# Each "app" in Django is like a Laravel "package" or "module"
# ============================================================
INSTALLED_APPS = [
    'django.contrib.admin',        # Built-in admin panel (Laravel has no equivalent — you'd use Nova/Filament)
    'django.contrib.auth',         # Authentication system (like Laravel's built-in Auth)
    'django.contrib.contenttypes', # Content type framework
    'django.contrib.sessions',     # Session handling (like Laravel's session driver)
    'django.contrib.messages',     # Flash messages (like Laravel's session()->flash())
    'django.contrib.staticfiles',  # Static file serving (like Laravel Mix / Vite)
    # Our custom apps (like Laravel packages/modules you create)
    'accounts',                    # User registration & profile management
    'tasks',                       # Core task management features
]


# ============================================================
# MIDDLEWARE = Like Laravel's app/Http/Kernel.php $middleware array
# Runs on every request, just like Laravel middleware
# ============================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',            # Like Laravel's TrustProxies
    'django.contrib.sessions.middleware.SessionMiddleware',     # Like StartSession
    'django.middleware.common.CommonMiddleware',                # URL normalization
    'django.middleware.csrf.CsrfViewMiddleware',               # Like VerifyCsrfToken
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Attaches user to request
    'django.contrib.messages.middleware.MessageMiddleware',     # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Security header
]

# Like Laravel's RouteServiceProvider — points to the root URL config
ROOT_URLCONF = 'taskmanager.urls'

# ============================================================
# TEMPLATES = Like Laravel's config/view.php
# Django uses its own template engine (similar to Blade)
# ============================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Like Laravel's resources/views/
        'APP_DIRS': True,                   # Also look in each app's templates/ folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'taskmanager.wsgi.application'


# ============================================================
# DATABASE = Like Laravel's config/database.php + .env DB settings
# Using SQLite for simplicity (like Laravel's default SQLite option)
# ============================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Laravel: DB_CONNECTION=sqlite
        'NAME': BASE_DIR / 'db.sqlite3',          # Laravel: DB_DATABASE
    }
}


# Password validation (like Laravel's password rules in validation)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# Like Laravel's public/ folder for assets
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ============================================================
# AUTH SETTINGS
# Like Laravel's config/auth.php
# ============================================================
LOGIN_URL = '/accounts/login/'           # Where to redirect if not logged in
LOGIN_REDIRECT_URL = '/dashboard/'       # Where to go after login
LOGOUT_REDIRECT_URL = '/accounts/login/' # Where to go after logout

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
