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
from ..models.item import Item
from ..models.user import User


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

    # >>> This is where 'engine' should be defined <<<
    engine = get_engine(settings) # Make sure this line exists and is correctly called

    # Create tables if they don't exist
    Base.metadata.create_all(engine)

    # >>> 'session_factory' should be created after 'engine' is defined <<<
    session_factory = get_session_factory(engine) # This was the problematic area

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        # Alternatively, if you've configured DBSession globally:
        # DBSession.configure(bind=engine)
        # dbsession = DBSession()

        # Check if admin already exists
        admin = dbsession.query(User).filter_by(username='admin').first()
        if not admin:
            admin_user = User(username='admin')
            admin_user.set_password('adminpassword') # Ganti dengan password yang kuat
            dbsession.add(admin_user)
            print("Admin user created with username 'admin' and password 'adminpassword'")
        else:
            print("Admin user already exists.")

        # Contoh menambahkan item awal (opsional)
        if dbsession.query(Item).count() == 0:
            item1 = Item(name='Contoh Item 1', description='Deskripsi item pertama')
            item2 = Item(name='Contoh Item 2', description='Deskripsi item kedua')
            dbsession.add_all([item1, item2])
            print("Sample items created.")
        else:
            print("Items already exist or table is not empty.")

# If you have any code outside the main() function that tries to use 'engine'
# or 'session_factory', it needs to be moved inside main() or have these
# variables passed to it.