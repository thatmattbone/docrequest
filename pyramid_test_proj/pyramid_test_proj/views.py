from pyramid.view import view_config

from docrequest import docrequest_pyramid as docrequest


@view_config(route_name='decorated_without_definitions', renderer='string')
@docrequest
def decorated_without_definitions(request):
    """
    A view decorated with `@docrequest` that does not define any
    parameters.

    This should run just like normal.
    """
    return """Hello World"""


@view_config(route_name='simple_docrequest', renderer='string')
@docrequest
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
@docrequest
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

@view_config(route_name='choices_docrequest', renderer='json')
@docrequest
def choices_docrequest(request, intchoice, strchoice, floatchoice):
    """
    Demonstrating the docrequest choices syntax.

    docrequest:
     - intchoice:int<2,3,5,7>
     - strchoice:str<foo, bar, baz>
     - floatchoice:float<39.39, 42.42>
    """
    return {'intchoice': intchoice,
            'strchoice': strchoice,
            'floatchoice': floatchoice}


@view_config(route_name='choices_docrequest_sphinx', renderer='json')
@docrequest
def choices_docrequest_sphinx(request, intchoice, strchoice, floatchoice):
    """
    Demonstrating the choices syntax, sphinx version.

    docrequest:

    :param int<2,3,5,7> intchoice: an integer
    :param str<foo, bar, baz> strchoice: a str
    :param float<39.39, 42.42> floatchoice: a float
    """
    return {'intchoice': intchoice,
            'strchoice': strchoice,
            'floatchoice': floatchoice}


#    :param [int] value4: list of values
