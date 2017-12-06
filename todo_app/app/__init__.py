# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask import request, jsonify, abort, make_response

from instance.config import app_config

# initialize sql-alchemy orm
db = SQLAlchemy()

def create_app(config_name):

    from models import Todo, User

    app = FlaskAPI(__name__)
    app.config.from_object(app_config[config_name])
    #app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from app.models import Todo
    @app.route('/todos/', methods=['POST', 'GET'])
    def todos():
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated

                if request.method == "POST":
                    name = str(request.data.get('name', ''))
                    if name:
                        todo = Todo(name=name, created_by=user_id)
                        todo.save()
                        response = jsonify({
                            'id': todo.id,
                            'name': todo.name,
                            'date_created': todo.date_created,
                            'date_modified': todo.date_modified,
                            'created_by': user_id
                        })

                        return make_response(response), 201

                else:
                    # GET all the todos created by this user
                    todos = Todo.query.filter_by(created_by=user_id).order_by(desc(Todo.date_created))
                    results = []

                    for todo in todos:
                        obj = {
                            'id': todo.id,
                            'name': todo.name,
                            'date_created': todo.date_created,
                            'date_modified': todo.date_modified,
                            'created_by': todo.created_by
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401


    @app.route('/todos/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def todo_manipulation(id, **kwargs):
     # retrieve a todo using it's ID
        todo = Todo.query.filter_by(id=id).first()
        if not todo:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            todo.delete()
            return {
            "message": "todo {} deleted successfully".format(todo.id)
         }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            todo.name = name
            todo.contents = request.data.get('contents','')
            todo.save()
            response = jsonify({
                'id': todo.id,
                'name': todo.name,
                'content':todo.contents,
                'date_created': todo.date_created,
                'date_modified': todo.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': todo.id,
                'name': todo.name,
                'content':todo.contents,
                'date_created': todo.date_created,
                'date_modified': todo.date_modified
            })
            response.status_code = 200
            return response

    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
