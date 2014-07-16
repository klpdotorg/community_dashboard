# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('aksharaklp.reports.views',
    url(r'^$', 'reports', name='reports'))
