from django.http import HttpResponse

from docrequest import docrequest

@docrequest(framework="django")
def my_view(request):
    return HttpResponse("hello world", content_type="text/plain")


@docrequest(framework="django")
def simple_request(request, value1, value2):
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
