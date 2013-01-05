from pyramid.config import Configurator


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    
    config.add_route('decorated_without_definitions', '/decorated-without-definitions')
    config.add_route('simple_docrequest', '/simple-docrequest')
    config.add_route('simple_docrequest_sphinx', '/simple-docrequest-sphinx')

    config.scan()
    return config.make_wsgi_app()
