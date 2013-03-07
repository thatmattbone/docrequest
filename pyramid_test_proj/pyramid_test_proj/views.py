from pyramid.view import view_config

from docrequest import docrequest_pyramid as docrequest
from docrequest import readable_type


@view_config(route_name='decorated_without_definitions', renderer='string')
@docrequest
def decorated_without_definitions(request):
    """
    A view decorated with `@docrequest` that does not define any
    parameters.

    This should run just like normal.
    """
    return """Hello World"""


@view_config(route_name='simple_docrequest', renderer='json')
@docrequest
def simple_docrequest(request, value1, value2):
    """
    Simple example using docrequest syntax.

    docrequest:
      - value1:int
      - value2:str
    """
    return {'value1': {'value': value1,
                       'type': readable_type(value1)},
            'value2': {'value': value2,
                       'type': readable_type(value2)}}


@view_config(route_name='simple_docrequest_sphinx', renderer='json')
@docrequest
def simple_docrequest_sphinx(request, value1, value2):
    """
    Simple example using sphinx syntax.

    docrequest:

    :param int value1: the first value
    :param str value2: the second value
    """
    return {'value1': {'value': value1,
                       'type': readable_type(value1)},
            'value2': {'value': value2,
                       'type': readable_type(value2)}}


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


@view_config(route_name='list_docrequest', renderer='json')
@docrequest
def list_docrequest(request, intlist, strlist, floatlist):
    """
    Demonstrating the list syntax, sphinx version.

    docrequest:
     - intlist:[int]
     - strlist:[str]
     - floatlist:[float]
    """
    return {'intlist': intlist,
            'strlist': strlist,
            'floatlist': floatlist,
            }


@view_config(route_name='list_docrequest_sphinx', renderer='json')
@docrequest
def list_docrequest_sphinx(request, intlist, strlist, floatlist):
    """
    Demonstrating the list syntax, sphinx version.

    docrequest:

    :param [int] intlist: an integer
    :param [str] strlist: a str
    :param [float] floatlist: a float
    """

    return {'intlist': intlist,
            'strlist': strlist,
            'floatlist': floatlist}


@view_config(route_name='with_url_param', renderer='json')
@docrequest
def with_url_param(request, testint):
    """
    Mixin' with url parameters.

    docrequest:
      - testint:int
    """
    return {'url_param': int(request.matchdict['url_param']),
            'testint': testint}
