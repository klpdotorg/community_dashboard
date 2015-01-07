# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib import admin

urlpatterns = patterns('',
	(r'^reports/', include('aksharaklp.reports.urls')),
	(r'^fileuploadapp/', include('aksharaklp.fileuploadapp.urls')),
	(r'^admin/', include(admin.site.urls)), 
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
