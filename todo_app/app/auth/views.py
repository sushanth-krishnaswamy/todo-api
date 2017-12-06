# /app/auth/views.py

from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User

class RegistrationView(MethodView):
    """New User registration."""

    def post(self):
        """ POST Url -> /auth/register"""

        # Check if the user already exosts
        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            # If no use, register them
            try:
                post_data = request.data

                # Register the user
                email = post_data['email']
                password = post_data['password']

                user = User(email=email, password=password)
                user.save()

                response = {
                    'message': 'You have registered successfully. You may now login!.'
                }
                # return a response notifying the user that they registered successfully
                return make_response(jsonify(response)), 201
            except Exception as e:

                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # User already exists
            response = {
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 202




class LoginView(MethodView):
    """User login and access token generation."""

    def post(self):
        """ POST Url --> /auth/login"""
        try:
            user = User.query.filter_by(email=request.data['email']).first()

            if user and user.password_is_valid(request.data['password']):
                #generating access token
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You have logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                # User does not exist.
                response = {
                    'message': 'Invalid email or password, Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500


registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')

#auth blueprint rule for auth/register
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

#auth blueprint rule for auth/login
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
