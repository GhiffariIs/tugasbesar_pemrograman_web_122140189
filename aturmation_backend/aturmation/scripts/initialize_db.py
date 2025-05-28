import argparse
import sys
from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .. import models


def setup_models(dbsession):
    """
    Add or update models / fixtures in the database.
    """
    # Create an admin user if no users exist
    user_count = dbsession.query(models.User).count()
    if user_count == 0:
        admin = models.User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin')
        dbsession.add(admin)
    
    # Create some sample categories
    category_count = dbsession.query(models.Category).count()
    if category_count == 0:
        categories = [
            models.Category(nama_kategori='Electronics'),
            models.Category(nama_kategori='Clothing'),
            models.Category(nama_kategori='Books'),
            models.Category(nama_kategori='Food & Beverages'),
            models.Category(nama_kategori='Sports & Outdoor')
        ]
        dbsession.add_all(categories)


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
            setup_models(dbsession)
    except OperationalError:
        print('''
Database could not be initialized. Are you sure it exists?

To initialize a new database:
1. Create a database in PostgreSQL
2. Update the sqlalchemy.url setting in your .ini file
3. Run "initialize_db" again
        ''')


if __name__ == '__main__':
    main()
