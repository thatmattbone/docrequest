from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^decorated-without-definitions$', 'testapp.views.decorated_without_definitions'),
    url(r'^simple-docrequest$', 'testapp.views.simple_docrequest'),
    url(r'^simple-docrequest-sphinx$', 'testapp.views.simple_docrequest_sphinx'),
    url(r'^choices-docrequest-sphinx$', 'testapp.views.choices_docrequest_sphinx'),
    url(r'^choices-docrequest$', 'testapp.views.choices_docrequest'),
)
