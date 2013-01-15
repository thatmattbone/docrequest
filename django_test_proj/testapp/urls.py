from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^decorated-without-definitions$', 'testapp.views.decorated_without_definitions'),
    url(r'^simple-request$', 'testapp.views.simple_request'),

)
