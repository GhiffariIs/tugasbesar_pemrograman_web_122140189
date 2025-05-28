import argparse
import sys
import transaction

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from ..models import Base, DBSession
from ..models.user import User

def setup_models(dbsession):
    """
    Add or update models
    """
    # Create admin user if it doesn't exist
    admin = dbsession.query(User).filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            name='Administrator',
            email='admin@aturmation.com',
            role='admin'
        )
        admin.set_password('admin123')
        dbsession.add(admin)
    
    # Create staff user if it doesn't exist
    staff = dbsession.query(User).filter_by(username='staff').first()
    if not staff:
        staff = User(
            username='staff',
            name='Staff Demo',
            email='staff@aturmation.com',
            role='staff'
        )
        staff.set_password('staff123')
        dbsession.add(staff)

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])

def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            Base.metadata.create_all(dbsession.bind)
            setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.
The problem might be caused by one of the following things:

1. You may need to initialize your database tables with 
   'initialize_db development.ini'.
   
2. Your database server may not be running. Please check that 
   the database server referred to by the
   'sqlalchemy.url' setting in your 'development.ini' file is running.
        ''')

if __name__ == '__main__':
    main()
