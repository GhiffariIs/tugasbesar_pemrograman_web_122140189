import os
import sys
from waitress import serve
from pyramid.paster import get_app

# Get the absolute path of the directory containing this script
parent_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)

# Default config file
config_file = os.path.join(parent_dir, 'development.ini')

# Get the WSGI application
app = get_app(config_file)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6543))
    host = os.environ.get('HOST', 'localhost')
    
    print(f"Starting server on http://{host}:{port}")
    print("To exit press CTRL+C")
    
    serve(app, host=host, port=port)
