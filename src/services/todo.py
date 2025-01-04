from bson import ObjectId, json_util
from flask import Response, jsonify, request
from src.config.mongodb import mongo
from pymongo.errors import PyMongoError


def create_todo_service():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "The request body is empty",
                "data": None
            }), 400


        title = data.get("title")
        if not title:
            return jsonify({
                "status": "error",
                "message": "The 'title' field is required",
                "data": None
            }), 400
            
        # Get 'description', optional if not provided        
        description = data.get("description", None)

        # Insert the new document into the database
        response = mongo.db.todos.insert_one({
            "title": title,
            "description": description,
            "done": False
        })

        # Build a success response
        return jsonify({
            "status": "success",
            "message": "Todo created successfully",
            "data": {
                "id": str(response.inserted_id),
                "title": title,
                "description": description,
                "done": False
            }
        }), 201
    except PyMongoError as e:
        # Handle MongoDB-specific errors
        return jsonify({
            "status": "error",
            "message": f"Database interaction error: {str(e)}",
            "data": None
        }), 500
    except Exception as e:
        # Handle other unexpected errors
        return jsonify({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}",
            "data": None
        }), 500

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
