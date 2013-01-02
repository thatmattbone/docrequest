from pyramid.view import view_config

from docrequest import docrequest

@view_config(route_name='home', renderer='string')
@docrequest
def my_view(request):
    """
    My docstring.
    """
    return """Hello World"""
