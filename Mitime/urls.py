"""
URL configuration for Mitime project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from .ckviews import custom_upload_file

handler500 = "core.views.err500_view"
handler404 = "core.views.err404_view"
handler403 = "core.views.err403_view"
handler401 = "core.views.err401_view"
handler400 = "core.views.err400_view"

urlpatterns = [
    path('', include('core.urls')),
    # path('admin/', admin.site.urls),
]

urlpatterns += [
    path('ckeditor5/image_upload/', custom_upload_file, name='ckeditor5_custom_upload_file'),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
