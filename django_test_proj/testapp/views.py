import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from docrequest import docrequest_django as docrequest


@docrequest
def decorated_without_definitions(request):
    """
    A view decorated with `@docrequest()` that does not define any
    parameters.

    This should run just like normal.
    """
    return HttpResponse("Hello World", content_type="text/plain")

@csrf_exempt
@docrequest
def simple_docrequest(request, value1, value2):
    """
    A simple POST example.

    docrequest:
      - value1:int
      - value2:str
    """
    response = "{value1}:{value1_type}, {value2}:{value2_type}"

    response = response.format(value1=value1, value1_type=str(type(value1)), 
                               value2=value2, value2_type=str(type(value2)))

    return HttpResponse(response, content_type="text/plain")

@csrf_exempt
@docrequest
def simple_docrequest_sphinx(request, value1, value2):
    """
    Simple example using sphinx syntax.

    docrequest:

    :param int value1: the first value
    :param str value2: the second value
    """
    response = "{value1}:{value1_type}, {value2}:{value2_type}"

    response = response.format(value1=value1, value1_type=str(type(value1)),
                               value2=value2, value2_type=str(type(value2)))

    return HttpResponse(response, content_type="text/plain")


@docrequest
def choices_docrequest(request, intchoice, strchoice, floatchoice):
    """
    Demonstrating the docrequest choices syntax.

    docrequest:
     - intchoice:int<2,3,5,7>
     - strchoice:str<foo, bar, baz>
     - floatchoice:float<39.39, 42.42>
    """
    return HttpResponse(json.dumps({'intchoice': intchoice,
                                    'strchoice': strchoice,
                                    'floatchoice': floatchoice}), content_type="application/json")


@docrequest
def choices_docrequest_sphinx(request, intchoice, strchoice, floatchoice):
    """
    Demonstrating the choices syntax, sphinx version.

    docrequest:

    :param int<2,3,5,7> intchoice: an integer
    :param str<foo, bar, baz> strchoice: a str
    :param float<39.39, 42.42> floatchoice: a float
    """
    return HttpResponse(json.dumps({'intchoice': intchoice,
                                    'strchoice': strchoice,
                                    'floatchoice': floatchoice}), content_type="application/json")