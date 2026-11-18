from django.contrib import admin
from django.urls import include, path

app_name = "MyM"

urlpatterns = [
    urlpatterns = [
        path("admin/", admin.site.urls),
        path("MyM/", include("apps.MyM.urls")),
    ]
]