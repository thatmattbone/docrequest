from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^my-view$', 'testapp.views.my_view'),
    url(r'^simple-request$', 'testapp.views.simple_request'),
)
