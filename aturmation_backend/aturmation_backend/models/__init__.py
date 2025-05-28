from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import register

# Basis untuk model deklaratif SQLAlchemy
Base = declarative_base()

# Fungsi untuk mengikat mesin SQLAlchemy ke sesi
def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory

# Fungsi untuk mendapatkan mesin SQLAlchemy dari pengaturan
def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)

# Fungsi untuk menyertakan model dalam konfigurasi Pyramid
def includeme(config):
    """
    Initialize the model for a Pyramid app.
    """
    settings = config.get_settings()
    # Setup SQLAlchemy engine and session factory
    engine = get_engine(settings)
    session_factory = get_session_factory(engine)

    # Membuat sesi per permintaan
    config.registry['dbsession_factory'] = session_factory
    config.add_request_method(
        lambda r: session_factory(),
        'dbsession',
        reify=True
    )
    # Mendaftarkan sesi dengan zope.sqlalchemy untuk manajemen transaksi
    # Jika Anda menggunakan pyramid_tm
    # register(session_factory)

    # Membuat semua tabel yang didefinisikan oleh model (jika belum ada)
    # Ini biasanya dilakukan oleh alat migrasi seperti Alembic dalam produksi
    Base.metadata.create_all(engine)