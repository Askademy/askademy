from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(("api.urls"))),
    path("", include("web.urls")),
]

if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('media/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    ]