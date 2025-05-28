from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPCreated, HTTPOk, HTTPNoContent
from sqlalchemy.exc import DBAPIError

from ..models.item import Item

@view_config(route_name='api_items_collection', request_method='GET', renderer='json', permission='view')
def get_items(request):
    try:
        items = request.dbsession.query(Item).all()
        return {'items': [item.as_dict() for item in items]}
    except DBAPIError:
        return Response("Database error", content_type='text/plain', status=500)

@view_config(route_name='api_items_collection', request_method='POST', renderer='json', permission='create')
def create_item(request):
    try:
        data = request.json_body
        name = data.get('name')
        description = data.get('description')

        if not name:
            raise HTTPBadRequest("Name is required")

        new_item = Item(name=name, description=description)
        request.dbsession.add(new_item)
        request.dbsession.flush() # Untuk mendapatkan ID sebelum commit
        return HTTPCreated(json_body={'message': 'Item created successfully', 'item': new_item.as_dict()})
    except DBAPIError:
        request.dbsession.rollback()
        return Response("Database error", content_type='text/plain', status=500)
    except ValueError as e: # Jika json_body gagal parse
        return HTTPBadRequest(str(e))

@view_config(route_name='api_item_detail', request_method='GET', renderer='json', permission='view')
def get_item(request):
    item_id = request.matchdict['id']
    try:
        item = request.dbsession.query(Item).get(item_id)
        if item is None:
            raise HTTPNotFound("Item not found")
        return {'item': item.as_dict()}
    except DBAPIError:
        return Response("Database error", content_type='text/plain', status=500)

@view_config(route_name='api_item_detail', request_method='PUT', renderer='json', permission='edit')
def update_item(request):
    item_id = request.matchdict['id']
    try:
        item = request.dbsession.query(Item).get(item_id)
        if item is None:
            raise HTTPNotFound("Item not found")

        data = request.json_body
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        # updated_at akan diupdate oleh trigger atau onupdate di model

        request.dbsession.flush()
        return HTTPOk(json_body={'message': 'Item updated successfully', 'item': item.as_dict()})
    except DBAPIError:
        request.dbsession.rollback()
        return Response("Database error", content_type='text/plain', status=500)
    except ValueError as e:
        return HTTPBadRequest(str(e))

@view_config(route_name='api_item_detail', request_method='DELETE', renderer='json', permission='delete')
def delete_item(request):
    item_id = request.matchdict['id']
    try:
        item = request.dbsession.query(Item).get(item_id)
        if item is None:
            raise HTTPNotFound("Item not found")

        request.dbsession.delete(item)
        request.dbsession.flush()
        return HTTPNoContent(body=b'') # 204 No Content
    except DBAPIError:
        request.dbsession.rollback()
        return Response("Database error", content_type='text/plain', status=500)