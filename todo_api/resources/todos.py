from flask import Blueprint, abort, request, jsonify

from flask_restful import (Resource, Api)
# for marshaling responses
from flask_marshmallow import Marshmallow

# for parsing requests arguments
import webargs
from webargs.flaskparser import parser

from ..auth import auth
from .. import models
#import app

todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
mm = Marshmallow(todos_api)


def get_todo_or_404(id):
    try:
        todo = models.Todo.get(models.Todo.id == id)
    except models.Todo.DoesNotExist:
        abort(404)
    else:
        return todo


class TodoSchema(mm.Schema):
    class Meta:
        fields = ('id', 'name', 'completed', 'created_at',
                  '_links'
                  )
        strict = True

    # because of the blueprint the api endpoints have to be
    # '.<endpoint>' istead of '<endpoint>'
    _links = mm.Hyperlinks({
       'all':  mm.URLFor('.todos',  _scheme='http', _external=True),
       'self': mm.URLFor('.todo', id='<id>', _scheme='http', _external=True)
    })

    #removed the envelope, since this works better with the Angular app

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


todo_put_args = {
   'name': webargs.fields.Str(),
   'completed': webargs.fields.Bool()
}

todo_post_args = {
   'name': webargs.fields.Str(required=True),
   'completed': webargs.fields.Bool()
}


class TodoListAPI(Resource):
    @auth.login_required
    def get(self):
        all_todos = models.Todo.select()
        result = todos_schema.dump(all_todos)
        return jsonify(result.data)

    @auth.login_required
    def post(self):
        args = parser.parse(todo_post_args, request)
        todo = models.Todo.create(**args)
        result = todo_schema.dump(todo)
        return (result.data, 201)



class TodoAPI(Resource):
    @auth.login_required
    def get(self, id):
        todo = get_todo_or_404(id)
        result = todo_schema.dump(todo)
        return result.data

    @auth.login_required
    def put(self, id):
        args = parser.parse(todo_put_args, request)
        query = models.Todo.update(**args).where(models.Todo.id == id)
        query.execute()
        todo = get_todo_or_404(id)
        result = todo_schema.dump(todo)
        return result.data

    @auth.login_required
    def delete(self, id):
        query = models.Todo.delete().where(models.Todo.id==id)
        query.execute()
        return ('', 204)

api.add_resource(TodoListAPI, '/todos', endpoint='todos')
api.add_resource(TodoAPI, '/todos/<int:id>', endpoint='todo')