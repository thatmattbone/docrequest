import re
import colander

schema_type_mappings = {
    'int': colander.Int,
    'str': colander.Str,
}


def schema_node_for_line(line):
    result = re.match("\W*-\W*(?P<variable_name>\w+):(?P<variable_type>\w+)", line)
    if not result:
        raise Exception("docrequest definition {line} is invalid.".format(line=line))

    variable_name = result.groupdict()['variable_name']
    variable_type = result.groupdict()['variable_type']
    
    if variable_type in schema_type_mappings:
        return colander.SchemaNode(schema_type_mappings[variable_type]())
    else:
        raise Exception("Uknown variable type {}".format(variable_type))


def args_from_request(reqest, docrequest_definitions):
    return [1, 'two']


def docrequest(original_func):
    """
    Decorator for docrequest-enabled view functions.
    """
    def new_func(request):
        
        docstring = original_func.__doc__
        docstring = [line.strip() for line in docstring.split("\n")]
        
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
            args = args_from_request(request, docrequest_definitions)
            args.insert(0, request)
            
            context = original_func(*args)  # TODO support for kwargs, defaults, etc

        else:
            context = original_func(request)

        return context

    new_func.__name__ = original_func.__name__
    new_func.__doc__ = original_func.__doc__
    new_func.__dict__.update(original_func.__dict__)

    return new_func

