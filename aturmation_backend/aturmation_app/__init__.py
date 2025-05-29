# aturmation_app/__init__.py
from pyramid.config import Configurator

def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pyramid_tm')
        # config.include('pyramid_cors')
        config.add_tween('aturmation_app.tweens.cors_tween_factory')
        config.include('.security')
        config.include('.routes') # Memuat rute-rute

        # config.scan() di sini akan memindai seluruh paket aturmation_app.
        # Jika routes.py Anda sudah memiliki config.scan('.views'),
        # itu sudah cukup untuk view di dalam paket .views.
        # Memiliki config.scan() di sini sebagai catch-all juga tidak masalah.
        config.scan() 
    return config.make_wsgi_app()