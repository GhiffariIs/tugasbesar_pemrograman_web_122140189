from pyramid.view import view_config
from pyramid.response import Response
from pyramid.exceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPForbidden
from .models.user import User
from .security import authenticate

@view_config(route_name='home', renderer='json', request_method='GET')
def home_view(request):
    return {'project': 'aturmation_backend', 'status': 'running'}

@view_config(route_name='protected_example', renderer='json', permission='view')
def protected_view_example(request):
    return {'message': 'Anda memiliki akses ke sumber daya yang diproteksi ini.'}

@view_config(route_name='users', request_method='GET', renderer='json')
def get_users(request):
    users = User.get_all()
    return {'users': users}

@view_config(route_name='user', request_method='GET', renderer='json')
def get_user(request):
    user_id = request.matchdict.get('id')
    user = User.get_by_id(user_id)
    if user is None:
        raise HTTPNotFound("User not found")
    return user

@view_config(route_name='user', request_method='POST', renderer='json')
def create_user(request):
    data = request.json_body
    user = User.create(data['username'], data['password'])
    return Response(status=201, json_body=user)

@view_config(route_name='user', request_method='PUT', renderer='json')
def update_user(request):
    user_id = request.matchdict.get('id')
    data = request.json_body
    user = User.update(user_id, data['username'], data['password'])
    if user is None:
        raise HTTPNotFound("User not found")
    return user

@view_config(route_name='user', request_method='DELETE', renderer='json')
def delete_user(request):
    user_id = request.matchdict.get('id')
    success = User.delete(user_id)
    if not success:
        raise HTTPNotFound("User not found")
    return Response(status=204)