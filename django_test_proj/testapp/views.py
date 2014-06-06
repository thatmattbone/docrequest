import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from docrequest import docrequest_django as docrequest
from docrequest import readable_type


@csrf_exempt
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
    Simple example using sphinx syntax.

    docrequest:

    :param int value1: the first value
    :param str value2: the second value
    """
    response = json.dumps({'value1': {'value': value1,
                                      'type': readable_type(value1)},
                           'value2': {'value': value2,
                                      'type': readable_type(value2)}})

    return HttpResponse(response, content_type="application/json")


@csrf_exempt
@docrequest
def choices_docrequest(request, intchoice, strchoice, floatchoice):
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


@csrf_exempt
@docrequest
def list_docrequest(request, intlist, strlist, floatlist):
    """
    Demonstrating the list syntax, sphinx version.

    docrequest:

    :param [int] intlist: an integer
    :param [str] strlist: a str
    :param [float] floatlist: a float
    """
    return HttpResponse(json.dumps({'intlist': intlist,
                                    'strlist': strlist,
                                    'floatlist': floatlist}), content_type="application/json")


@csrf_exempt
@docrequest
def with_url_param(request, url_param, testint):
    """
    Mixin' with url parameters.

    docrequest:

    :param int testint:
    """
    return HttpResponse(json.dumps({'url_param': int(url_param),
                                    'testint': testint}))


@csrf_exempt
@docrequest
def with_multiple_url_params(request, param1, param2, testint):
    """
    Mixin' with url parameters.

    docrequest:

    :param int testint:
    """
    return HttpResponse(json.dumps({'param1': param1,
                                    'param2': param2,
                                    'testint': testint
                                    }))
