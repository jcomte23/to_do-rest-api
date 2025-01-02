from bson import ObjectId, json_util
from flask import Response, request
from config.mongodb import mongo


def create_todo_service():
    data = request.get_json()

    title = data.get("title", None)
    description = data.get("description", None)

    if title:
        response = mongo.db.todos.insert_one({
            "title": title,
            "description": description,
            "done": False
        })

        return {
            'id': str(response.inserted_id),
            'title': title,
            'description': description,
            'done': False
        }
    else:
        'Invalid payload', 400


def get_todos_service():
    data = mongo.db.todos.find()
    result = json_util.dumps(data)
    return Response(result, mimetype="application/json")


def get_todo_service(id):
    data = mongo.db.todos.find_one(
        {
            "_id": ObjectId(id)
        }
    )
    result = json_util.dumps(data)
    return Response(result, mimetype="application/json")


def update_todo_service(id):
    data = request.get_json()

    response = mongo.db.todos.update_one(
        {
            '_id': ObjectId(id)
        },
        {
            "$set": data
        }
    )

    if response.modified_count >= 1:
        return "todo updated succesfully", 200
    else:
        return 'todo not found', 404


def delete_todo_service(id):
    response = mongo.db.todos.delete_one({
        "_id": ObjectId(id)
    })

    if response.deleted_count >= 1:
        return 'Todo deleted successfully', 200
