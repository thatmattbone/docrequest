import inspect
import re
import colander

docrequest_schema_type_mappings = {
    'int': colander.Int,
    'str': colander.Str,
}


sphinx_schema_type_mappings = {
    'integer': colander.Int,
}    


def schema_node_for_line(line):
    result = re.match("\W*-\W*(?P<variable_name>\w+):(?P<variable_type>\w+)", line)
    if not result:
        raise Exception("docrequest definition {line} is invalid.".format(line=line))

    variable_name = result.groupdict()['variable_name']
    variable_type = result.groupdict()['variable_type']
    
    if variable_type in docrequest_schema_type_mappings:
        return colander.SchemaNode(docrequest_schema_type_mappings[variable_type](),
                                   name=variable_name)
    else:
        raise Exception("Uknown variable type {}".format(variable_type))


def args_from_request_pyramid(request, docrequest_definitions):
    schema = colander.SchemaNode(colander.Mapping())
    for line in docrequest_definitions:
        schema.add(schema_node_for_line(line))

    params = None
    if request.method == 'POST':
        params = request.POST
    elif request.method == 'GET':
        params = request.params

    deserialized = schema.deserialize(params)

    return deserialized


def args_from_request_django(request, docrequest_definitions):
    schema = colander.SchemaNode(colander.Mapping())
    for line in docrequest_definitions:
        schema.add(schema_node_for_line(line))

    params = None
    if request.method == 'POST':
        params = request.POST
    elif request.method == 'GET':
        params = request.GET

    deserialized = schema.deserialize(params.dict())

    return deserialized
    

class DocRequest(object):

    def __init__(self, framework="pyramid"):
        self.framework = framework


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
                # TODO refactor this, it's clunky and the code is copy-pasta
                if self.framework == "pyramid":
                    args = args_from_request_pyramid(request, docrequest_definitions)
                elif self.framework == "django":
                    args = args_from_request_django(request, docrequest_definitions)
                else:
                    raise Exception("Unknown framework {}".format(self.framework))

                context = original_func(request, **args)  # TODO support for args, defaults, etc

            else:
                context = original_func(request)

            return context

        new_func.__name__ = original_func.__name__
        new_func.__doc__ = original_func.__doc__
        new_func.__dict__.update(original_func.__dict__)

        return new_func
docrequest = DocRequest
