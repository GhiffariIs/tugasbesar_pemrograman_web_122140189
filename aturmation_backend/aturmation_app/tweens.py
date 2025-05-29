# aturmation_app/tweens.py
from pyramid.settings import aslist

def cors_tween_factory(handler, registry):
    """A tween factory that adds CORS headers to all responses."""

    allowed_origins = aslist(registry.settings.get('cors.manual.origins', '*'))
    allow_all_origins = '*' in allowed_origins

    def cors_tween(request):
        # Tangani Preflight (OPTIONS) requests
        if request.method == 'OPTIONS':
            response = request.response
            # Periksa apakah origin request diizinkan
            origin = request.headers.get('Origin')
            if allow_all_origins or (origin and origin in allowed_origins):
                response.headers['Access-Control-Allow-Origin'] = origin if not allow_all_origins else '*'
                response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, PUT, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization'
                response.headers['Access-Control-Max-Age'] = '3600' # Cache preflight selama 1 jam
                response.headers['Access-Control-Allow-Credentials'] = 'true'
            # Jika origin tidak diizinkan untuk OPTIONS, biarkan Pyramid menangani (biasanya 403/404)
            return response

        # Untuk request aktual
        try:
            response = handler(request)
        except Exception as e:
            # Jika ada exception sebelum respons dibuat, kita tidak bisa tambah header.
            # Biarkan exception handler Pyramid yang bekerja.
            raise

        # Tambahkan header ke semua respons normal
        origin = request.headers.get('Origin')
        if allow_all_origins:
            response.headers['Access-Control-Allow-Origin'] = '*'
        elif origin and origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin

        # Header lain yang mungkin dibutuhkan (beberapa mungkin sudah ada dari pyramid_cors jika aktif)
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        # response.headers.vary.add('Origin') # Penting jika tidak '*'

        return response
    return cors_tween