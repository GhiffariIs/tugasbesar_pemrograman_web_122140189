import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'plaster_pastedeploy',
    'pyramid >= 1.9',
    'pyramid_jinja2', # Jika menggunakan Jinja2
    'pyramid_debugtoolbar',
    'waitress',
    'sqlalchemy',
    'psycopg2-binary', # Driver PostgreSQL
    'pyramid_tm', # Untuk manajemen transaksi (opsional, tapi direkomendasikan dengan SQLAlchemy)
    'zope.sqlalchemy', # Untuk integrasi SQLAlchemy dengan pyramid_tm
    'passlib', # <--- TAMBAHKAN INI
    'pyramid_sqlalchemy',
    'pyramid_restful', # <--- TAMBAHKAN INI
    # Tambahkan dependensi lain di sini
]

tests_require = [
    'WebTest >= 1.3.1',  # untuk pengujian fungsional
    'pytest',  # atau nose
    'pytest-cov', # untuk coverage
]

setup(
    name='aturmation_backend',
    version='0.0',
    description='Backend untuk Aturmation',
    long_description=README,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Nama Anda',
    author_email='email@anda.com',
    url='',
    keywords='web pyramid pylons sqlalchemy',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = aturmation_backend:main',
        ],
        'console_scripts': [
            'initialize_aturmation_backend_db = aturmation_backend.scripts.initializedb:main',
        ],
    },
)