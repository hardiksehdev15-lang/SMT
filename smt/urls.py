from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # 🔒 Hardened admin (obfuscated via settings.ADMIN_URL)
    path(settings.ADMIN_URL, admin.site.urls),

    # Core site pages
    path("", include("sehdev.urls")),

    # App-level routing
    path("products/", include("products.urls")),
    path("enquiry/", include("enquiries.urls")),

    # -------- LEGACY REDIRECTS (DO NOT REMOVE ABRUPTLY) --------
    path(
        "home/",
        RedirectView.as_view(url="/", permanent=True),
    ),
    path(
        "home/home/",
        RedirectView.as_view(url="/", permanent=True),
    ),
]

# Media served ONLY in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
