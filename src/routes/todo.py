from flask import Blueprint

from services.todo import create_todo_service


todo = Blueprint('todo',__name__)

@todo.route('/')
def get_todos():
    return "get all todos"

@todo.route('/id')
def get_todo(id):
    return "get todo by an id"

@todo.route('/', methods=['POST'])
def create_todo():
    return create_todo_service()

@todo.route('/<id>', methods=['PUT'])
def update_todo(id):
    return "update todo"

@todo.route('/<id>', methods=['DELETE'])
def delete_todo(id):
    return "delete todo"