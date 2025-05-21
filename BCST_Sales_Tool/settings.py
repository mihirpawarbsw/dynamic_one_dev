
from decouple import config
import os
from pathlib import Path
# APPEND_SLASH = False
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Get the environment (local or production)
# LIST=['local','production_test','production']
ENVIRONMENT = config('ENVIRONMENT', default='local')
# ENVIRONMENT = config('ENVIRONMENT', default='production_test')
# ENVIRONMENT = config('ENVIRONMENT', default='production_test2')
# ENVIRONMENT = config('ENVIRONMENT', default='production')
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # or cache or another
DEBUG = True if ENVIRONMENT == 'local' else False
if ENVIRONMENT == 'local':
    print('#################################################################')
    print('local ENVIRONMENT->',ENVIRONMENT)
    print('#################################################################')
    # Local database settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'bcs_sales_tracker',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',   
            'PORT': '3306',
        }    
    }
    # Local static files settings
    STATIC_URL = '/static/'
    STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # Local allowed hosts (typically just localhost)
    ALLOWED_HOSTS = ['127.0.0.1']
    ROOT_URLCONF = 'BCST_Sales_Tool.urls'
    WSGI_APPLICATION = 'BCST_Sales_Tool.wsgi.application'
    # Set home page redirect url
    SESSION_EXPIRE_REDIRECT_URL='/'
    LOGOUT_REDIRECT_URL='/login_with_password'
    # LOGOUT_REDIRECT_URL='http://apps.brand-scapes.com/onedashboard/'
    BASE_REDIRECT_URL='/'

    # Excel and file read url
    # 1 minute expressed in seconds (1 * 60)
    # 15 minute expressed in seconds (10 * 60)
    SESSION_COOKIE_AGE = 60 * 60
    TEMP_UPLOAD="uploaded_data/temp_data/" #FOR LOCAL MACHINE USE THIS PATH
    TEMP_UPLOAD_COPIED="uploaded_data/Users_data/" #FOR LOCAL MACHINE USE THIS PATH  
    PYTHONPATH_MARKET_MASTER = r"uploaded_data/Market_Master/"
    PYTHONPATH="uploaded_data/transform_data/" #FOR LOCAL MACHINE USE THIS PATH
    ORIGINAL_DATA="uploaded_data/original_data/" #FOR LOCAL MACHINE USE THIS PATH
    TEMP_UPLOAD="uploaded_data/temp_data/" #FOR LOCAL MACHINE USE THIS PATH
    SELLOUT_UPLOAD="uploaded_data/sellout/" #FOR SELLOUT USE THIS PATH
    SKU_UPLOAD="uploaded_data/sku/" #FOR SKU USE THIS PATH
    DOORS_UPLOAD="uploaded_data/doors/" #FOR DOORS USE THIS PATH
    PYTHONPATH_JSON=r'uploaded_data\*.json' #FOR LOCAL MACHINE USE THIS PATH
    MERGED_PYTHONPATH="merged_pythonpath/" #FOR LOCAL MACHINE USE THIS PATH
    MERGED_PYTHONPATH_JSON=r'merged_pythonpath\*.json' #FOR LOCAL MACHINE USE THIS PATH
    FINAL_CROSSTAB_OUTPUT="static/download_cross_table_excel/" 
 
elif ENVIRONMENT == 'production_test':
    print('#################################################################')
    print('production_test ENVIRONMENT->',ENVIRONMENT)
    print('#################################################################')
    # Production database settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'bcs_sales_tracker',
            'USER': 'root',
            'PASSWORD': 'Calen#2024',
            'HOST': 'localhost',   
            'PORT': '3306',
        }    
    }
    # Production static files settings
    STATIC_URL = '/static/'
    STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # Production allowed hosts
    ALLOWED_HOSTS = ['dynamicviewtest.brand-scapes.com']
    CSRF_TRUSTED_ORIGINS = ['https://dynamicviewtest.brand-scapes.com','http://apps.brand-scapes.com']
    CORS_ORIGIN_WHITELIST = ['https://dynamicviewtest.brand-scapes.com','http://apps.brand-scapes.com']

    ROOT_URLCONF = 'BCST_Sales_Tool.urls'
    WSGI_APPLICATION = 'BCST_Sales_Tool.wsgi.application'
    # Set home page redirect url
    LOGOUT_REDIRECT_URL='http://apps.brand-scapes.com/onedashboard/logout'
    BASE_REDIRECT_URL='https://dynamicviewtest.brand-scapes.com/'
    #SESSION_COOKIE_SECURE = True
    #CSRF_COOKIE_SECURE = True    
    # Excel and file read url
    # 1 minute expressed in seconds (1 * 60)
    # 20 minute expressed in seconds (20 * 60)
    SESSION_COOKIE_AGE = 15 * 60
    TEMP_UPLOAD="/var/www/html/dynamicviewtest/BCST_Sales_Tool/uploaded_data/temp_data/" #FOR LOCAL MACHINE USE THIS PATH
    TEMP_UPLOAD_COPIED="/var/www/html/dynamicviewtest/BCST_Sales_Tool/uploaded_data/Users_data/" #FOR LOCAL MACHINE USE THIS PATH  
    PYTHONPATH_MARKET_MASTER = r"/var/www/html/dynamicviewtest/BCST_Sales_Tool/uploaded_data/Market_Master/"
    PYTHONPATH=r"/var/www/html/dynamicviewtest/BCST_Sales_Tool/uploaded_data/transform_data/" #FOR LOCAL MACHINE USE THIS PATH
    ORIGINAL_DATA=r"/var/www/html/dynamicviewtest/BCST_Sales_Tool/uploaded_data/original_data/" #FOR LOCAL MACHINE USE THIS PATH
    TEMP_UPLOAD=r"/var/www/html/dynamicviewtest/BCST_Sales_Tool/uploaded_data/temp_data/" #FOR LOCAL MACHINE USE THIS PATH
    PYTHONPATH_JSON=r"/var/www/html/dynamicviewtest/BCST_Sales_Tool/uploaded_data\*.json" #FOR LOCAL MACHINE USE THIS PATH

    MERGED_PYTHONPATH=r"/var/www/html/dynamicviewtest/BCST_Sales_Tool/merged_pythonpath/" #FOR LOCAL MACHINE USE THIS PATH
    MERGED_PYTHONPATH_JSON=r"/var/www/html/dynamicviewtest/BCST_Sales_Tool/merged_pythonpath\*.json" #FOR LOCAL MACHINE USE THIS PATH
    FINAL_CROSSTAB_OUTPUT=r"/var/www/html/dynamicviewtest/BCST_Sales_Tool/static/download_cross_table_excel/"
elif ENVIRONMENT == 'production_test2':
    print('#################################################################')
    print('production ENVIRONMENT->',ENVIRONMENT)
    print('#################################################################')

    # Production database settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'bcs_sales_tracker',
            'USER': 'root',
            'PASSWORD': 'Calen#2024',
            'HOST': 'localhost',   
            'PORT': '3306',
        }    
    }
    # Production static files settings
    STATIC_URL = '/static/'
    STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # Production allowed hosts
    ALLOWED_HOSTS = ['dynamicview.brand-scapes.com']
    ROOT_URLCONF = 'BCST_Sales_Tool_demo.urls'
    WSGI_APPLICATION = 'BCST_Sales_Tool_demo.wsgi.application'
    # Set home page redirect url
    LOGOUT_REDIRECT_URL='http://apps.brand-scapes.com/onedashboard/logout'
    BASE_REDIRECT_URL='https://bsstrackertest.brand-scapes.com/'

    # Excel and file read url
    # 1 minute expressed in seconds (1 * 60)
    # 20 minute expressed in seconds (20 * 60)
    SESSION_COOKIE_AGE = 15 * 60
    TEMP_UPLOAD="/var/www/html/bsstracker/BCST_Sales_Tool_demo/uploaded_data/temp_data/" #FOR LOCAL MACHINE USE THIS PATH
    TEMP_UPLOAD_COPIED="/var/www/html/bsstracker/BCST_Sales_Tool_demo/uploaded_data/Users_data/" #FOR LOCAL MACHINE USE THIS PATH    
    PYTHONPATH_MARKET_MASTER = r"/var/www/html/bsstracker/BCST_Sales_Tool_demo/uploaded_data/Market_Master/"
    PYTHONPATH=r"/var/www/html/bsstracker/BCST_Sales_Tool_demo/uploaded_data/transform_data/" #FOR LOCAL MACHINE USE THIS PATH
    ORIGINAL_DATA=r"/var/www/html/bsstracker/BCST_Sales_Tool_demo/uploaded_data/original_data/" #FOR LOCAL MACHINE USE THIS PATH
    TEMP_UPLOAD=r"/var/www/html/bsstracker/BCST_Sales_Tool_demo/uploaded_data/temp_data/" #FOR LOCAL MACHINE USE THIS PATH
    PYTHONPATH_JSON=r"/var/www/html/bsstracker/BCST_Sales_Tool_demo/uploaded_data\*.json" #FOR LOCAL MACHINE USE THIS PATH

    MERGED_PYTHONPATH=r"/var/www/html/bsstracker/BCST_Sales_Tool_demo/merged_pythonpath/" #FOR LOCAL MACHINE USE THIS PATH
    MERGED_PYTHONPATH_JSON=r"/var/www/html/bsstracker/BCST_Sales_Tool_demo/merged_pythonpath\*.json" #FOR LOCAL MACHINE USE THIS PATH
    FINAL_CROSSTAB_OUTPUT=r"/var/www/html/bsstracker/BCST_Sales_Tool_demo/static/download_cross_table_excel/"

elif ENVIRONMENT == 'production':
    print('#################################################################')
    print('production ENVIRONMENT->',ENVIRONMENT)
    print('#################################################################')

    # Production database settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'bcs_sales_tracker',
            'USER': 'root',
            'PASSWORD': 'Calen#2024',
            'HOST': 'localhost',   
            'PORT': '3306',
        }    
    }
    # Production static files settings
    STATIC_URL = '/static/'
    STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # Production allowed hosts
    ALLOWED_HOSTS = ['dynamicview.brand-scapes.com']
    ROOT_URLCONF = 'BCST_Sales_Tool_live.urls'
    WSGI_APPLICATION = 'BCST_Sales_Tool_live.wsgi.application'
    # Set home page redirect url
    LOGOUT_REDIRECT_URL='https://shiseido.brand-scapes.com/logout'
    BASE_REDIRECT_URL='https://dynamicview.brand-scapes.com/'

    # Excel and file read url
    # 1 minute expressed in seconds (1 * 60)
    # 20 minute expressed in seconds (20 * 60)
    SESSION_COOKIE_AGE = 15 * 60
    PYTHONPATH_MARKET_MASTER = r"/var/www/html/dynamicview/BCST_Sales_Tool_live/uploaded_data/Market_Master/"  
    PYTHONPATH=r"/var/www/html/dynamicview/BCST_Sales_Tool_live/uploaded_data/transform_data/" #FOR LOCAL MACHINE USE THIS PATH
    ORIGINAL_DATA=r"/var/www/html/dynamicview/BCST_Sales_Tool_live/uploaded_data/original_data/" #FOR LOCAL MACHINE USE THIS PATH
    TEMP_UPLOAD=r"/var/www/html/dynamicview/BCST_Sales_Tool_live/uploaded_data/temp_data/" #FOR LOCAL MACHINE USE THIS PATH
    PYTHONPATH_JSON=r"/var/www/html/dynamicview/BCST_Sales_Tool_live/uploaded_data\*.json" #FOR LOCAL MACHINE USE THIS PATH

    MERGED_PYTHONPATH=r"/var/www/html/dynamicview/BCST_Sales_Tool_live/merged_pythonpath/" #FOR LOCAL MACHINE USE THIS PATH
    MERGED_PYTHONPATH_JSON=r"/var/www/html/dynamicview/BCST_Sales_Tool_live/merged_pythonpath\*.json" #FOR LOCAL MACHINE USE THIS PATH
    FINAL_CROSSTAB_OUTPUT=r"/var/www/html/dynamicview/BCST_Sales_Tool_live/static/download_cross_table_excel/"
 

pythonpath = r"C:/python project/BCST_Sales_Tool//"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z#0b+a5oy2ib#40*%2^51&_+8k+)@()z+8z9%g0*_f36is0p+_'
BASE_URL_LOCAL='/loginwith_password'


# Optional settings for additional security
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
DATA_UPLOAD_MAX_MEMORY_SIZE=None
IMG_OUTPUT_PYTHONPATH = "static/chart_image_crosstab/"

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main_dashboard',
    'login',
    'rest_framework',
    # 'Demo_app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'login.AutoLogoutMiddleware_file.AutoLogoutMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # 'login.middleware.PageVisitLogMiddleware',
]





TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = 'en-us'  # or 'en-in' if you prefer Indian English
USE_I18N = True
USE_TZ = True
TIME_ZONE = 'Asia/Kolkata'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

