def includeme(config):
    """
    Initialize security for our Pyramid application.
    """
    config.include('.jwt')
