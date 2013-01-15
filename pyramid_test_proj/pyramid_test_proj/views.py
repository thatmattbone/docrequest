from pyramid.view import view_config

from docrequest import docrequest


@view_config(route_name='decorated_without_definitions', renderer='string')
@docrequest()
def decorated_without_definitions(request):
    """
    A view decorated with `@docrequest()` that does not define any
    parameters.

    This should run just like normal.
    """
    return """Hello World"""


@view_config(route_name='simple_docrequest', renderer='string')
@docrequest()
def simple_docrequest(request, value1, value2):
    """
    Simple example using docrequest syntax.

    docrequest:
      - value1:int
      - value2:str
    """
    response = "{value1}:{value1_type}, {value2}:{value2_type}"

    return response.format(value1=value1, value1_type=str(type(value1)), 
                           value2=value2, value2_type=str(type(value2)))


@view_config(route_name='simple_docrequest_sphinx', renderer='string')
@docrequest()
def simple_docrequest_sphinx(request, value1, value2):
    """
    Simple example using sphinx syntax.

    docrequest:

    :param int value1: the first value
    :param str value2: the second value
    """
    response = "{value1}:{value1_type}, {value2}:{value2_type}"

    return response.format(value1=value1, value1_type=str(type(value1)), 
                           value2=value2, value2_type=str(type(value2)))


#    :param int<1,2,3> value3: choices value
#    :param [int] value4: list of values
