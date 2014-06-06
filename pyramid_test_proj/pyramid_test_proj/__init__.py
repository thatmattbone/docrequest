from pyramid.config import Configurator


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    
    config.add_route('decorated_without_definitions', '/decorated-without-definitions')

    config.add_route('simple_docrequest', '/simple-docrequest')

    config.add_route('choices_docrequest', '/choices-docrequest')

    config.add_route('list_docrequest', '/list-docrequest')

    config.add_route('with_url_param', '/with-url-param/{url_param}')

    config.scan()
    return config.make_wsgi_app()
