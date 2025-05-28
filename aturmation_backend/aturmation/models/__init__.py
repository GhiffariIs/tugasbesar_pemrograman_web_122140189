from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import register

# Recommended naming convention for SQLAlchemy
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)
DBSession = scoped_session(sessionmaker())
register(DBSession)


def includeme(config):
    """Initialize database."""
    settings = config.get_settings()
    
    from sqlalchemy import engine_from_config
    
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
