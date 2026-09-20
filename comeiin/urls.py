# comeiin/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from core.views import favicon_view


urlpatterns = [
    path('admin/', admin.site.urls),

    # Favicon
    path('favicon.ico', favicon_view, name='favicon'),


    # allauth — sign in, signup, Google OAuth
    path('accounts/', include('allauth.urls')),
    path('', include('pwa.urls')),
    # Core — home, about, privacy, PWA manifest, PWA service worker
    path('', include('core.urls')),

    # Products
    path('products/', include('products.urls')),

    # Quotes
    path('quote/', include('quotes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)