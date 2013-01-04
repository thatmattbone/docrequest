from pyramid.view import view_config

from docrequest import docrequest

@view_config(route_name='home', renderer='string')
@docrequest
def my_view(request):
    """
    My docstring.
    """
    return """Hello World"""

@view_config(route_name='simple_request', renderer='string')
@docrequest
def simple_request(request, value1, value2):
    """
    A simple POST example.

    docrequest:
      - value1:int
      - value2:str
    """
    response = "{value1}:{value1_type}, {value2}:{value2_type}"

    return response.format(value1=value1, value1_type=str(type(value1)), 
                           value2=value2, value2_type=str(type(value2)))
