# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = patterns('',
	(r'^reports/', include('aksharaklp.reports.urls')),
	(r'^fileuploadapp/', include('aksharaklp.fileuploadapp.urls')), # Just for ease of use.
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
