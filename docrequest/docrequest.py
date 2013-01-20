import inspect
import re
import colander

DOCREQUEST_SCHEMA_TYPE_MAPPINGS = {
    'int': colander.Int,
    'str': colander.Str,
    'float': colander.Float,
}


SPHINX_SCHEMA_TYPE_MAPPINGS = {
    'int': colander.Int,
    'str': colander.Str,
    'float': colander.Float,
}


DOCREQUEST_DEFINITION = re.compile("\W*-\W*(?P<variable_name>\w+):(?P<variable_type>\w+)")
SPHINX_DEFINITION = re.compile("\W*:param\W+(?P<variable_type>\w+)\W+(?P<variable_name>\w+):\W*(?P<variable_description>\w+)\W*")

def schema_node_for_line(line):
    result = DOCREQUEST_DEFINITION.match(line)

    if not result:
        result = SPHINX_DEFINITION.match(line)
    
    if not result:
        raise Exception("docrequest definition {line} is invalid.".format(line=line))

    variable_name = result.groupdict()['variable_name']
    variable_type = result.groupdict()['variable_type']
    
    if variable_type in DOCREQUEST_SCHEMA_TYPE_MAPPINGS:
        return colander.SchemaNode(DOCREQUEST_SCHEMA_TYPE_MAPPINGS[variable_type](),
                                   name=variable_name)
    else:
        raise Exception("Unknown variable type {}".format(variable_type))


class PyramidFrameworkAdapter(object):
    def get_params_from_request(self, request):
        params = None
        if request.method == 'POST':
            params = request.POST
        elif request.method == 'GET':
            params = request.params
        else:
            raise NotImplementedError("Unsupported HTTP method {}".format(request.method))

        return params


class DjangoFrameworkAdapter(object):
    def get_params_from_request(self, request):
        params = None
        if request.method == 'POST':
            params = request.POST
        elif request.method == 'GET':
            params = request.GET
        else:
            raise NotImplementedError("Unsupported HTTP method {}".format(request.method))

        return params.dict()
    

class DocRequest(object):

    def __init__(self, framework="pyramid"):

        framework_adapters = {'pyramid': PyramidFrameworkAdapter,
                              'django': DjangoFrameworkAdapter}

        if framework in framework_adapters:
            self.framework = framework_adapters[framework]()
        else:
            raise Exception("Unknown framework {}".format(framework))


    def __call__(self, original_func):
        """
        Decorator for docrequest-enabled view functions.
        """

        if not inspect.isfunction(original_func):
            raise Exception("""{func} is not a function. It sucks, but for now you need to call the docrequest decorator with parens like this: @docrequest(). Could that be it?""".format(func=original_func))
        
        def new_func(request):
            docstring = original_func.__doc__
            if docstring is not None:
                docstring = [line.strip() for line in docstring.split("\n")]
            else:
                docstring = []

            recording_docrequest_definitions = None
            docrequest_definitions = []
            for line in docstring:
                if line == "docrequest:":
                    if recording_docrequest_definitions == True:
                        raise Exception("Two docrequest blocks detected!")
                    else:
                        recording_docrequest_definitions = True
                else:
                    if recording_docrequest_definitions and line:
                        docrequest_definitions.append(line)

            if docrequest_definitions:
                schema = colander.SchemaNode(colander.Mapping())
                for line in docrequest_definitions:
                    schema.add(schema_node_for_line(line))

                params = self.framework.get_params_from_request(request)
                args = schema.deserialize(params)

                context = original_func(request, **args)  # TODO support for args, defaults, etc

            else:
                context = original_func(request)

            return context

        new_func.__name__ = original_func.__name__
        new_func.__doc__ = original_func.__doc__
        new_func.__dict__.update(original_func.__dict__)

        return new_func

docrequest_pyramid = DocRequest(framework="pyramid")
docrequest_django = DocRequest(framework="django")