def includeme(config):
    """
    Initialize views for our Pyramid application.
    """
    config.scan('.auth')
    config.scan('.category')
    config.scan('.product')
    config.scan('.transaction')
