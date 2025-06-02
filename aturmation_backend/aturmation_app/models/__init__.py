# aturmation_app/models/__init__.py
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers

# import or define all models here to ensure they are attached to the
# Base.metadata prior to any initialization routines
from .user import User  # flake8: noqa
from .product import Product  # flake8: noqa

# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('aturmation_app.models')``.

    """
    settings = config.get_settings()

    # create session factory and register it
    session_factory = get_session_factory(get_engine(settings))
    config.registry['dbsession_factory'] = session_factory

    # make request.dbsession available for use in Pyramid views
    config.add_request_method(
        # Simple session factory without transaction manager
        lambda r: session_factory(),
        'dbsession',
        reify=True
    )