import django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import userauth.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('userauth/', include('userauth.urls')),
    path('order/', include('order.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
