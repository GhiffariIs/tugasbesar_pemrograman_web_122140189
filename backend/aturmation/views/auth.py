from pyramid.view import view_defaults, view_config
from ..models.user import User
from .base import BaseView
from pyramid.security import remember, forget
import json


@view_defaults(route_name='auth', renderer='json')
class AuthView(BaseView):
    
    @view_config(request_method='POST', route_name='login')
    def login(self):
        try:
            body = self.request.json_body
            username = body.get('username')
            password = body.get('password')
            
            if not username or not password:
                return self.error_response("Username and password are required", 400)
            
            user = self.dbsession.query(User).filter_by(username=username).first()
            if not user or not user.check_password(password):
                return self.error_response("Invalid username or password", 401)
            
            # Generate JWT token
            token = self.request.auth_policy.generate_token(user.id)
            
            return self.json_response({
                'token': token,
                'user': user.to_dict()
            })
        except Exception as e:
            return self.error_response(str(e), 500)
            
    @view_config(request_method='POST', route_name='register')
    def register(self):
        try:
            body = self.request.json_body
            username = body.get('username')
            email = body.get('email')
            password = body.get('password')
            
            if not username or not email or not password:
                return self.error_response("Username, email and password are required", 400)
            
            # Check if user already exists
            existing_user = self.dbsession.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                field = "username" if existing_user.username == username else "email"
                return self.error_response(f"This {field} is already in use", 400)
            
            # Create new user
            user = User(username=username, email=email)
            user.set_password(password)
            
            # Set first user as admin
            if self.dbsession.query(User).count() == 0:
                user.is_admin = True
                
            self.dbsession.add(user)
            self.dbsession.flush()  # To get the user ID
            
            # Generate JWT token
            token = self.request.auth_policy.generate_token(user.id)
            
            return self.json_response({
                'token': token,
                'user': user.to_dict()
            }, status=201)
            
        except Exception as e:
            return self.error_response(str(e), 500)
            
    @view_config(request_method='GET', route_name='user_info', permission='user')
    def get_user_info(self):
        try:
            return self.json_response(self.request.user.to_dict())
        except Exception as e:
            return self.error_response(str(e), 500)
            
    @view_config(request_method='POST', route_name='logout')
    def logout(self):
        try:
            # JWT is stateless, so we just tell the client to forget the token
            return self.json_response({"message": "Successfully logged out"})
        except Exception as e:
            return self.error_response(str(e), 500)
