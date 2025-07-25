"""
URL configuration for bcs project.

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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "autocomplete/core/",
        include("core.autocomplete_urls", "core_autocomplete"),
    ),
    path(
        "autocomplete/czapki",
        include("czapki.autocomplete_urls", "czapki_autocomplete"),
    ),
    path(
        "autocomplete/encyklopedia/",
        include("encyklopedia.autocomplete_urls", "encyklopedia_autocomplete"),
    ),
    path(
        "autocomplete/kalendarz/",
        include("kalendarz.autocomplete_urls", "kalendarz_autocomplete"),
    ),
    path(
        "autocomplete/kronika/",
        include("kronika.autocomplete_urls", "kronika_autocomplete"),
    ),
    path(
        "autocomplete/miejsca/",
        include("miejsca.autocomplete_urls", "miejsca_autocomplete"),
    ),
    path(
        "autocomplete/osoby/",
        include("osoby.autocomplete_urls", "osoby_autocomplete"),
    ),
    path(
        "autocomplete/prawo/",
        include("prawo.autocomplete_urls", "prawo_autocomplete"),
    ),
    path(
        "autocomplete/slowniczek_lacinski/",
        include(
            "slowniczek_lacinski.autocomplete_urls",
            "slowniczek_lacinski_autocomplete",
        ),
    ),
    path(
        "autocomplete/zrodla/",
        include("zrodla.autocomplete_urls", "zrodla_autocomplete"),
    ),
    path("drzewo/", include("drzewo.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
