from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import Authenticated, Allow, Deny, Everyone
from .models.user import User
from .security import check_credentials

@view_config(route_name='user', request_method='GET', permission=Authenticated)
def get_users(request):
    users = User.get_all()
    return Response(json_body=[user.to_dict() for user in users])

@view_config(route_name='user', request_method='POST', permission=Authenticated)
def create_user(request):
    data = request.json_body
    user = User(username=data['username'], password=data['password'])
    user.save()
    return Response(status=201, json_body=user.to_dict())

@view_config(route_name='user', request_method='PUT', permission=Authenticated)
def update_user(request):
    user_id = request.matchdict['id']
    data = request.json_body
    user = User.get_by_id(user_id)
    if user:
        user.username = data.get('username', user.username)
        user.password = data.get('password', user.password)
        user.save()
        return Response(json_body=user.to_dict())
    return Response(status=404)

@view_config(route_name='user', request_method='DELETE', permission=Authenticated)
def delete_user(request):
    user_id = request.matchdict['id']
    user = User.get_by_id(user_id)
    if user:
        user.delete()
        return Response(status=204)
    return Response(status=404)

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    # Tambahkan rute untuk operasi CRUD Anda di sini nanti
    # Contoh:
    # config.add_route('items_api', '/api/v1/items')
    # config.add_route('item_api', '/api/v1/items/{id}')