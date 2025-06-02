# aturmation_app/scripts/initializedb.py
import os
import sys
import transaction

from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import get_engine # Impor dari models/__init__.py
from ..models.user import User, UserRole # Hanya User
from ..models.product import Product   # Hanya Product

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = get_engine(settings)

    # Hapus tabel lama jika ada untuk memastikan skema bersih (opsional untuk dev)
    # print("Dropping old tables (if they exist)...")
    # Base.metadata.drop_all(engine, tables=[User.__table__, Product.__table__])

    print("Creating new tables (User, Product)...")
    Base.metadata.create_all(engine) # Hanya membuat tabel User dan Product
    print("Tables created.")

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    dbsession = Session()

    with transaction.manager:
        # Buat Admin User
        admin = dbsession.query(User).filter_by(username='admin').first()
        if not admin:
            admin_user = User(
                name='Administrator',
                username='admin',
                email='admin@example.com', # Pastikan email unik
                role=UserRole.admin
            )
            admin_user.set_password('adminpassword')
            dbsession.add(admin_user)
            print("Admin user 'admin' created.")
        else:
            # Pastikan field baru ada jika admin sudah ada
            if not admin.name: admin.name = 'Administrator'
            if not admin.email: admin.email = 'admin@example.com'
            if not admin.role: admin.role = UserRole.admin
            print("Admin user 'admin' already exists. Ensured fields.")

        # Produk Contoh (tanpa kategori)
        if dbsession.query(Product).count() == 0:
            prod1 = Product(
                name='Produk Unggulan A', 
                sku='PUA001', 
                description='Deskripsi Produk Unggulan A.',
                price=150000.00,
                stock=20
            )
            prod2 = Product(
                name='Produk Standar B',
                sku='PSB002',
                description='Deskripsi Produk Standar B.',
                price=50000.00,
                stock=100
            )
            dbsession.add_all([prod1, prod2])
            print("Sample products created.")
        else:
            print("Products already exist.")
    
    dbsession.close()
    print("Database initialization finished.")