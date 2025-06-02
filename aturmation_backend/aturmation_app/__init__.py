# aturmation_app/__init__.py
from pyramid.config import Configurator

def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pyramid_tm')
        
        # Untuk CORS (pilih salah satu atau pastikan pyramid-cors terinstal jika di-include)
        # Jika pyramid-cors tidak bisa diinstal, Anda perlu implementasi tween manual di tweens.py
        # dan include tween tersebut di sini, serta hapus 'pyramid_cors' dari development.ini
        # config.include('pyramid_cors') 
        # atau
        # config.include('.tweens') # Jika Anda membuat tweens.py untuk CORS manual

        config.include('.security')
        config.include('.routes')
        
        config.scan() # Memindai semua view di paket aturmation_app dan sub-paketnya
    return config.make_wsgi_app()