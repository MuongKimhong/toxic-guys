from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

urlpatterns = [
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
