# aturmation_app/models/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .meta import Base # Pastikan Base diimpor
from .user import User, UserRole
from .product import Product # Hanya User dan Product

DBSession = scoped_session(sessionmaker())

def get_engine(settings, prefix='sqlalchemy.'):
    return create_engine(settings[prefix + 'url'])

def includeme(config):
    settings = config.get_settings()
    engine = get_engine(settings)
    DBSession.configure(bind=engine)
    config.add_request_method(
        lambda request: DBSession,
        'dbsession',
        reify=True
    )