import inspect
import re

import pyparsing
import colander

SCHEMA_TYPE_MAPPINGS = {
    'int': {'colander_class': colander.Int,
            'to_python': lambda x: int(x) },

    'str': {'colander_class': colander.Str,
            'to_python': lambda x: str(x) },

    'float': {'colander_class': colander.Float,
              'to_python': lambda x: float(x) },
}

docrequest_type = (pyparsing.Keyword('int') | pyparsing.Keyword('str') | pyparsing.Keyword('float'))\
    .setResultsName('docrequest_type')
docrequest_choices = (pyparsing.Literal("<") + pyparsing.delimitedList(pyparsing.Word(initChars=pyparsing.alphanums, bodyChars=pyparsing.alphanums + "."), combine=False) +">")\
    .setResultsName('docrequest_choices')
docrequest_type_with_choices = (docrequest_type + docrequest_choices)\
    .setResultsName('docrequest_type_with_choices')
docrequest_list_type = (pyparsing.Literal("[") + (docrequest_type_with_choices|docrequest_type) + "]")\
    .setResultsName("docrequest_list_type")
docrequest_description = pyparsing.OneOrMore(pyparsing.Word(initChars=pyparsing.alphanums, bodyChars=pyparsing.alphanums))\
    .setResultsName('docrequest_definition')
docrequest_variable = pyparsing.Word(initChars=pyparsing.alphas, bodyChars=pyparsing.alphanums)\
    .setResultsName('docrequest_variable')
docrequest_schema =  (docrequest_list_type|docrequest_type_with_choices|docrequest_type)

docrequest_sphinx = pyparsing.Literal(":") + "param" + docrequest_schema + docrequest_variable + ":" + docrequest_description
docrequest_docrequest = pyparsing.Literal("-") + docrequest_variable + ":" + docrequest_schema

docrequest_grammar = docrequest_sphinx|docrequest_docrequest


def schema_node_for_line(line):

    matches = docrequest_grammar.parseString(line)
    match_dict = matches.asDict()

    variable_type = match_dict['docrequest_type']
    variable_name = match_dict['docrequest_variable']

    if variable_type in SCHEMA_TYPE_MAPPINGS:
        schema_node = colander.SchemaNode(SCHEMA_TYPE_MAPPINGS[variable_type]['colander_class'](),
                                          name=variable_name)
    else:
        raise Exception("Unknown variable type {}".format(variable_type))

    if 'docrequest_choices' in match_dict:
        to_python = SCHEMA_TYPE_MAPPINGS[variable_type]['to_python']
        schema_node.validator = colander.OneOf([to_python(x) for x in match_dict['docrequest_choices'][1:-1]])

    if 'docrequest_list_type' in match_dict:
        child_node = schema_node
        schema_node = colander.SchemaNode(colander.Sequence(), child_node, accept_scalar=True, name=variable_name)

    return schema_node


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
            raise Exception("""{func} is not a function.""".format(func=original_func))
        
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

        #TODO replace with functools wraps?
        new_func.__name__ = original_func.__name__
        new_func.__doc__ = original_func.__doc__
        new_func.__dict__.update(original_func.__dict__)

        return new_func

docrequest_pyramid = DocRequest(framework="pyramid")
docrequest_django = DocRequest(framework="django")


def readable_type(obj):
    """
    Return a readable type of the obj that's independent of python 2 vs 3.
    """
    if isinstance(obj, type(0)):
        return 'int'
    elif isinstance(obj, type(u"")):
        return 'str'

