from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("api-users/", include("users.urls")),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
