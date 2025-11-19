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
from django.views.generic import RedirectView

from bcs.settings import STATIC_URL

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "favicon.ico",
        RedirectView.as_view(
            url=STATIC_URL + "images/favicon.ico", permanent=True
        ),
    ),
    path("_nested_admin/", include("nested_admin.urls")),
    path("dashboard/", include(arg="dashboard.urls", namespace="dashboard")),
    path("drzewo/", include(arg="drzewo.urls", namespace="drzewo")),
    path("spiewnik/", include(arg="spiewnik.urls", namespace="spiewnik")),
    path("miejsca/", include(arg="miejsca.urls", namespace="miejsca")),
    path(
        "wyszukiwarka/",
        include(arg="wyszukiwarka.urls", namespace="wyszukiwarka"),
    ),
    path(
        "autocomplete/czapki",
        include(
            arg="czapki.autocomplete_urls", namespace="czapki_autocomplete"
        ),
    ),
    path(
        "autocomplete/dashboard",
        include(
            arg="dashboard.autocomplete_urls",
            namespace="dashboard_autocomplete",
        ),
    ),
    path(
        "autocomplete/encyklopedia/",
        include(
            arg="encyklopedia.autocomplete_urls",
            namespace="encyklopedia_autocomplete",
        ),
    ),
    path(
        "autocomplete/honory/",
        include(
            arg="honory.autocomplete_urls", namespace="honory_autocomplete"
        ),
    ),
    path(
        "autocomplete/kalendarz/",
        include(
            arg="kalendarz.autocomplete_urls",
            namespace="kalendarz_autocomplete",
        ),
    ),
    path(
        "autocomplete/kronika/",
        include(
            arg="kronika.autocomplete_urls", namespace="kronika_autocomplete"
        ),
    ),
    path(
        "autocomplete/miejsca/",
        include(
            arg="miejsca.autocomplete_urls", namespace="miejsca_autocomplete"
        ),
    ),
    path(
        "autocomplete/multimedia/",
        include(
            arg="multimedia.autocomplete_urls",
            namespace="multimedia_autocomplete",
        ),
    ),
    path(
        "autocomplete/osoby/",
        include(arg="osoby.autocomplete_urls", namespace="osoby_autocomplete"),
    ),
    path(
        "autocomplete/prawo/",
        include(arg="prawo.autocomplete_urls", namespace="prawo_autocomplete"),
    ),
    path(
        "autocomplete/skarbiec/",
        include(
            arg="skarbiec.autocomplete_urls", namespace="skarbiec_autocomplete"
        ),
    ),
    path(
        "autocomplete/slowniczek_lacinski/",
        include(
            arg="slowniczek_lacinski.autocomplete_urls",
            namespace="slowniczek_lacinski_autocomplete",
        ),
    ),
    path(
        "autocomplete/spiewnik/",
        include(
            arg="spiewnik.autocomplete_urls",
            namespace="spiewnik_autocomplete",
        ),
    ),
    path(
        "autocomplete/zrodla/",
        include(
            arg="zrodla.autocomplete_urls", namespace="zrodla_autocomplete"
        ),
    ),
]

urlpatterns += static(
    prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
