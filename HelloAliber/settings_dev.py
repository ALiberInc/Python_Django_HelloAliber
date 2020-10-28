from .settings_common import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']


def show_toolbar(request):
    return True


LOGGING = {
    'version': 1,  # 1固定
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        # <アプリケーション名>が利用するロガー
        'profile_app': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'accounts': {
            'handlers': ['console', 'file_accounts'],
            'level': 'DEBUG',
        }
    },
    # ハンドラの設定
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev'
        },
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

# 開発環境にメールの配信先をコンソールする設定
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}
