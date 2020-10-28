from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path, include
from . import settings_common, settings_dev

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('profile_app.urls')),
    path('accounts/', include('accounts.urls')),
#    path('accounts/', include('allauth.urls')),
]

if settings_dev.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
urlpatterns += static(settings_common.MEDIA_URL, document_root=settings_dev.MEDIA_ROOT)
