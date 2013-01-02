
def docrequest(original_func):
    """
    Some stuff...
    """
    def new_func(request):
        #context = original_func(*args[1:], **kwargs)  # HACK the args[1:] is because of the implied root_factory arg
        context = original_func(request)

        docstring = original_func.__doc__
        docstring = "\n".join([line.strip() for line in docstring.split("\n")])
    
        return context

    new_func.__name__ = original_func.__name__
    new_func.__doc__ = original_func.__doc__
    new_func.__dict__.update(original_func.__dict__)

    return new_func

