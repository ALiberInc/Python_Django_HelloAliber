from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path, include
from . import settings, settings_dev


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('profile_app.urls')),
    path('accounts/', include('accounts.urls')),
    path('asset_app/',include('asset_app.urls')),
#    path('accounts/', include('allauth.urls')),
]

if settings_dev.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    
urlpatterns += static(settings.MEDIA_URL, document_root=settings_dev.MEDIA_ROOT)
