# try:
from .settings_common import *
# except ImportError:
#    pass

# 環境変数からSECRET_KEYを取得する設定
SECRET_KEY = os.environ.get('SECRET_KEY')

# 環境変数からDEBUGを取得。デフォルトはTrue（本番環境モード）
DEBUG = int(os.environ.get('DEBUG', default=0))

# 許可するホストを記載
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# if not DEBUG:
#    import django_heroku
#   django_heroku.settings(locals())

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'jyrS$23Yta'
EMAIL_HOST_PASSWORD = 'Ning1488Google'
EMAIL_USE_TLS = False

LOGGING = {
    'version': 1,  # 1固定
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        # <アプリケーション名>が利用するロガー
        'profile_app': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'accounts': {
            'handlers': ['file_accounts'],
            'level': 'DEBUG',
        }
    },
    # ハンドラの設定
    'handlers': {
        'file': {  # どこに出すかの設定に名前をつける `file`という名前をつけている
            'level': 'INFO',  # INFO以上のログを取り扱うという意味
            'class': 'logging.FileHandler',  # ログを出力するためのクラスを指定
            'filename': os.path.join(BASE_DIR, 'HelloAliber_INFO.log', ),  # どこに出すか
            'formatter': 'all',  # どの出力フォーマットで出すかを名前で指定
            'encoding': 'utf-8',
        },
        'file_accounts': {  # どこに出すかの設定に名前をつける `file`という名前をつけている
            'level': 'INFO',  # INFO以上のログを取り扱うという意味
            'class': 'logging.FileHandler',  # ログを出力するためのクラスを指定
            'filename': os.path.join(BASE_DIR, 'HelloAliber_INFO.log', ),  # どこに出すか
            'formatter': 'all',  # どの出力フォーマットで出すかを名前で指定
            'encoding': 'utf-8',
        },
    },
    # フォーマッタの設定
    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
        'all': {  # 出力フォーマットに`all`という名前をつける
            'format': '\t'.join([
                "[%(levelname)s]",
                "asctime:%(asctime)s",
                "module:%(module)s",
                "message:%(message)s",
                "process:%(process)d",
                "thread:%(thread)d",
            ])
        },
    }
}

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DATABASE_DB', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('DATABASE_USER', 'user'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'password'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
    }
}

STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
