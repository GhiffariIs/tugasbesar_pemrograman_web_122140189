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
    User,
)
from ..models.user import UserRole
from ..models import (
    get_engine,
    get_session_factory,
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
    Base.metadata.create_all(engine)
    
    # Create a simple session without transaction manager
    session_factory = get_session_factory(engine)
    session = session_factory()
    
    try:
        # Add admin user if it doesn't exist
        admin = session.query(User).filter_by(username='admin').first()
        if not admin:
            admin = User(
                name='Administrator',
                username='admin',
                email='admin@example.com',
                role=UserRole.ADMIN
            )
            admin.set_password('adminpassword')
            session.add(admin)
            print("Added admin user")
        
        # Add a staff user
        staff = session.query(User).filter_by(username='staff').first()
        if not staff:
            staff = User(
                name='Staff User',
                username='staff',
                email='staff@example.com',
                role=UserRole.STAFF
            )
            staff.set_password('staffpassword')
            session.add(staff)
            print("Added staff user")
        
        # Commit changes manually
        session.commit()
        print("Database initialized successfully")
    except Exception as e:
        session.rollback()
        print(f"Error initializing database: {e}")
        raise
    finally:
        session.close()