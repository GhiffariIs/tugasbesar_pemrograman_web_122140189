from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        # Sertakan konfigurasi model (SQLAlchemy)
        config.include('.models') # Titik (.) merujuk ke paket saat ini

        # Sertakan pyramid_tm untuk manajemen transaksi per request
        config.include('pyramid_tm')

        # Sertakan konfigurasi security (autentikasi & otorisasi)
        config.include('.security') # Titik (.) merujuk ke paket saat ini

        # Sertakan Jinja2 jika Anda berencana menggunakan template HTML
        # config.include('pyramid_jinja2')

        # Sertakan rute dari routes.py
        config.include('.routes') # Titik (.) merujuk ke paket saat ini

        config.scan() # Memindai view dan konfigurasi lainnya
    return config.make_wsgi_app()