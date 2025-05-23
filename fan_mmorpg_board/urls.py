from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return redirect("users:home")


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("ads/", include("board.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("users/", include("users.urls")),
    path("accounts/", include("allauth.urls")),
    path("auth/", include("social_django.urls", namespace="social")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
