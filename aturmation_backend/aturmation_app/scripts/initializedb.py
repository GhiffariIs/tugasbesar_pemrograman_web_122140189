# aturmation_app/scripts/initializedb.py
import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    User,
    Product
)


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
    
    print("Creating new tables (User, Product)...")
    Base.metadata.create_all(engine)
    print("Tables created.")
    
    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        
        # Check if admin user already exists
        admin = dbsession.query(User).filter_by(username='admin').first()
        if not admin:
            admin = User(name='Administrator', username='admin', email='admin@example.com')
            admin.set_password('adminpassword')
            # Tetap berikan nilai role untuk kompatibilitas database
            admin.role = 'admin'  
            dbsession.add(admin)
            print("Admin user 'admin' created.")
        
        # Add some sample products if none exist
        product_count = dbsession.query(Product).count()
        if product_count == 0:
            # Tambahkan beberapa contoh produk
            products = [
                Product(
                    name="Laptop Gaming",
                    sku="LAP001",
                    description="Laptop gaming dengan performa tinggi",
                    price=12000000,
                    stock=10
                ),
                Product(
                    name="Smartphone Android",
                    sku="PHN001",
                    description="Smartphone dengan kamera 48MP",
                    price=3500000,
                    stock=25
                ),
                Product(
                    name="Wireless Earbuds",
                    sku="AUD001",
                    description="Earbuds tanpa kabel dengan noise cancelling",
                    price=1500000,
                    stock=30
                )
            ]
            
            for product in products:
                dbsession.add(product)
            
            print("Sample products created.")
    
    print("Database initialization finished.")