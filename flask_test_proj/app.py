from docrequest import docrequest_flask as docrequest
from docrequest import readable_type
from flask import Flask, jsonify
app = Flask(__name__)


@app.route("/decorated-without-definitions", methods=['GET', 'POST'])
@docrequest
def decorated_without_definitions():
    """
    A view decorated with `@docrequest()` that does not define any
    parameters.

    This should run just like normal.
    """
    return "Hello World"


@app.route("/simple-docrequest", methods=['GET', 'POST'])
@docrequest
def simple_docrequest(value1, value2):
    """
    Simple example using sphinx syntax.

    docrequest:

    :param int value1: the first value
    :param str value2: the second value
    """
    return jsonify({'value1': {'value': value1,
                               'type': readable_type(value1)},
                    'value2': {'value': value2,
                               'type': readable_type(value2)}})


@app.route("/choices-docrequest", methods=['GET', 'POST'])
@docrequest
def choices_docrequest(intchoice, strchoice, floatchoice):
    """
    Demonstrating the choices syntax, sphinx version.

    docrequest:

    :param int<2,3,5,7> intchoice: an integer
    :param str<foo, bar, baz> strchoice: a str
    :param float<39.39, 42.42> floatchoice: a float
    """
    return jsonify({'intchoice': intchoice,
                    'strchoice': strchoice,
                    'floatchoice': floatchoice})


@app.route("/list-docrequest", methods=['GET', 'POST'])
@docrequest
def list_docrequest(intlist, strlist, floatlist):
    """
    Demonstrating the list syntax, sphinx version.

    docrequest:

    :param [int] intlist: an integer
    :param [str] strlist: a str
    :param [float] floatlist: a float
    """
    return jsonify({'intlist': intlist,
                    'strlist': strlist,
                    'floatlist': floatlist})


@app.route("/with-url-param/{url_param}", methods=['GET', 'POST'])
@docrequest
def with_url_param(url_param, testint):
    """
    Mixin' with url parameters.

    docrequest:

    :param int testint:
    """
    return jsonify({'url_param': int(url_param),
                    'testint': testint})


# @app.route("")
# @docrequest
# def with_multiple_url_params(param1, param2, testint):
#     """
#     Mixin' with url parameters.
#
#     docrequest:
#
#     :param int testint:
#     """
#     return jsonify({'param1': param1,
#                     'param2': param2,
#                     'testint': testint})


if __name__ == "__main__":
    app.debug = True
    app.run()
