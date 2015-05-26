from django.conf.urls import patterns, include, url
from django.contrib import admin
from schedulizer.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'prototype.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', home),
#    url(r'^main\.css$', css),
    url(r'^main$', 'schedulizer.views.main', name='main'),
    url(r'^schedule$', make_schedule),
    url(r'^service$', 'schedulizer.views.service', name='service'),
    url(r'^staff$', 'schedulizer.views.staff', name='staff'),
    url(r'^contact$', 'schedulizer.views.contact', name='contact'),
    url(r'^about$', 'schedulizer.views.about', name='about'),
    url(r'^submit_form$', 'schedulizer.views.make_schedule',name="submit_form"),
    url(r'^recall/$', 'schedulizer.views.recall_schedule', name="recall"),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
