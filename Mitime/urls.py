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
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]
