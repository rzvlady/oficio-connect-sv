import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('servicios/', include('servicios.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', include('usuarios.urls')),
    path('servicios/', include(('servicios.urls', 'servicios'), namespace='servicios')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

