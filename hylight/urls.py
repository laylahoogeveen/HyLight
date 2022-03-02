from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("hl.urls")),
    path("admin/", admin.site.urls),
]
