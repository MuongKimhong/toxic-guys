from rest_framework_simplejwt.views import TokenRefreshView
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("api-users/", include("users.urls")),
    path("api-groups/", include("groups.urls")),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
