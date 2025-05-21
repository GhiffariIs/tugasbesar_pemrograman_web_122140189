from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers
import zope.sqlalchemy

# Import all models here for tables to be created
from .meta import Base
from .category import Category
from .product import Product
from .transaction import Transaction
from .user import User

# Run configure_mappers after all models have been imported
configure_mappers()


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager):
    """
    Get a ``sqlalchemy.orm.Session`` instance backed by a transaction.
    
    This function will hook the session to the transaction manager which
    will take care of committing any changes.
    """
    dbsession = session_factory()
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager
    )
    return dbsession


def includeme(config):
    """
    Initialize the model for a Pyramid app.
    
    Activate this setup by including ``config.include('aturmation.models')``.
    """
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    # Use sqlalchemy.url for backward compatibility
    # (could be removed in the future)
    engine = get_engine(settings)
    session_factory = get_session_factory(engine)
    config.registry['dbsession_factory'] = session_factory

    # Make request.dbsession available for use in Pyramid
    config.add_request_method(
        # r.tm is the transaction manager provided by pyramid_tm
        lambda r: get_tm_session(session_factory, r.tm),
        'dbsession',
        reify=True
    )