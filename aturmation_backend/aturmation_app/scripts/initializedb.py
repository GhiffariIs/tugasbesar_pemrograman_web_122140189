import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)
from pyramid.scripts.common import parse_vars

# Ensure these imports correctly point to your models and helper functions
from ..models.meta import Base
from ..models import (
    get_engine, # Make sure get_engine is imported
    get_session_factory,
    get_tm_session,
    DBSession # If you use DBSession directly for initialization, ensure it's configured
)
from ..models.user import User, UserRole
from ..models.category import Category
from ..models.product import Product
from ..models.transaction import Transaction, TransactionType

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

    # Buat semua tabel (termasuk user yang baru)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        admin = dbsession.query(User).filter_by(username='admin').first()
        if not admin:
            admin_user = User(
                name='Administrator', # Tambahkan nama
                username='admin',
                email='admin@example.com', # Tambahkan email
                role=UserRole.admin # Set role admin
            )
            admin_user.set_password('adminpassword') # Ganti dengan password yang kuat
            dbsession.add(admin_user)
            print("Admin user created with username 'admin', email 'admin@example.com', role 'admin', and password 'adminpassword'")
        else:
            # Jika admin sudah ada, pastikan field baru terisi (opsional, tergantung kebijakan Anda)
            if not admin.name:
                admin.name = 'Administrator'
            if not admin.email:
                admin.email = 'admin@example.com'
            if not admin.role:
                admin.role = UserRole.admin
            print("Admin user already exists. Ensure new fields are populated.")
