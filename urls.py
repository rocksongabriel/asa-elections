# -*- coding: utf-8 -*-
import aldryn_addons.urls
from aldryn_django.utils import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # add your own patterns here
    # path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('ec/admin/', admin.site.urls),

    path("", include("pages.urls", namespace="pages")),
    path("users/", include("users.urls", namespace="users")),
    path("voting/", include("vote_app.urls", namespace="vote_app")),

] + aldryn_addons.urls.patterns() + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
