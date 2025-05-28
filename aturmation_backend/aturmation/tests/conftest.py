import os
import sys
import pytest
from pyramid.paster import get_appsettings
from pyramid.testing import DummyRequest, testConfig
from pyramid import testing

from aturmation import main
from aturmation.models import get_engine, get_session_factory, get_tm_session
from aturmation.models.meta import Base

# Include the backend directory in sys.path 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


@pytest.fixture(scope='session')
def ini_file(request):
    # Get the SQLite URL for testing
    return os.path.join(os.path.dirname(__file__), '..', '..', 'test.ini')
