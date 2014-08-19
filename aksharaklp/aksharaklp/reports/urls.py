# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('aksharaklp.reports.views',
	url(r'^main/$', 'main', name='main'),
	url(r'^generate/$', 'generateReport', name='generateReport'),
	url(r'^experiment/$', 'experiment', name='experiment'))
