from setuptools import setup, find_packages

requires = [
    'pyramid',
    'pyramid_jinja2',
    'waitress',
    'psycopg2-binary',
    'sqlalchemy',
    'pyramid_tm',
    'pyramid_retry',
    'zope.sqlalchemy',
    'passlib',
    'bcrypt',
    'pyramid_jwt'
]

dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'pytest-cov',
]

setup(
    name='aturmation_app',
    version='0.0',
    description='Aturmation Backend Application',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
    entry_points={
        'paste.app_factory': [
            'main = aturmation_app:main',
        ],
        'console_scripts': [
            'initialize_aturmation_db = aturmation_app.scripts.initializedb:main',
        ],
    },
)