from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^decorated-without-definitions$', 'testapp.views.decorated_without_definitions'),

    url(r'^simple-docrequest$', 'testapp.views.simple_docrequest'),

    url(r'^choices-docrequest$', 'testapp.views.choices_docrequest'),

    url(r'^list-docrequest$', 'testapp.views.list_docrequest'),

    url(r'^with-url-param/(?P<url_param>\d+)$', 'testapp.views.with_url_param'),
    url(r'^with-multiple-url-params/(?P<param2>\d+)/(?P<param1>\d+)$', 'testapp.views.with_multiple_url_params'),
)
