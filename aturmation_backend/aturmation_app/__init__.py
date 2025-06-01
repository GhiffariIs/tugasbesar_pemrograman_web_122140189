# aturmation_app/__init__.py
from pyramid.config import Configurator

def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pyramid_tm')

        # Pastikan pyramid_cors sudah terinstal atau baris ini dikomentari jika belum
        # config.include('pyramid_cors') 

        config.include('.security')
        config.include('.routes') # Ini memuat definisi rute

        

        config.scan() 
    return config.make_wsgi_app()