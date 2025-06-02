from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import register

from .user import User, UserRole
from .category import Category
from .product import Product
from .transaction import Transaction, TransactionType

DBSession = scoped_session(sessionmaker())

def get_engine(settings, prefix='sqlalchemy.'):
    return create_engine(settings[prefix + 'url'])

def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory

def get_tm_session(session_factory, transaction_manager):
    dbsession = session_factory()
    register(dbsession, transaction_manager=transaction_manager)
    return dbsession

def includeme(config):
    """
    Inisialisasi model SQLAlchemy dan siapkan sesi database.
    Fungsi ini dipanggil oleh Pyramid saat aplikasi dimulai.
    """
    settings = config.get_settings()
    engine = get_engine(settings)
    session_factory = get_session_factory(engine)
    config.registry['dbsession_factory'] = session_factory

    # Membuat dbsession yang dapat diakses dari request
    config.add_request_method(
        lambda r: get_tm_session(session_factory, r.tm),
        'dbsession',
        reify=True
    )

    pass