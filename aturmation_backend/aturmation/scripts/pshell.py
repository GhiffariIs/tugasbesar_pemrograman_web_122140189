"""
Initialize Python shell for working with the project
"""
import os
import sys
import transaction

from pyramid.paster import get_appsettings
from pyramid.scripts.common import parse_vars

from ..models import DBSession, Base
from ..models.user import User
from ..models.category import Category
from ..models.product import Product
from ..models.transaction import Transaction, TransactionItem, TransactionType

def setup_app(env, argv=sys.argv):
    settings = get_appsettings(argv[1])
    setup_models = env["request"].registry.settings.get("setup_models", False)

    # Start a transaction
    with transaction.manager:
        # Pass the models we want to use in the shell
        env["tm"] = transaction.manager
        env["db"] = DBSession
        env["User"] = User
        env["Category"] = Category
        env["Product"] = Product
        env["Transaction"] = Transaction
        env["TransactionItem"] = TransactionItem
        env["TransactionType"] = TransactionType
