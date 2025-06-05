
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app_ecommerce.urls")),
    path('', include("authentication.urls")),
    path('dash/', include('app_ecommerce.urls', namespace='ecommerce')),
    path('dash/', include('authentication.urls', namespace='authentication')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
