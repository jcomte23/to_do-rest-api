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
                "data": None,
                "total_records": None,
            }), 400


        title = data.get("title")
        if not title:
            return jsonify({
                "status": "error",
                "message": "The 'title' field is required",
                "data": None,
                "total_records": None,
            }), 400
                  
        description = data.get("description", None)

        response = mongo.db.todos.insert_one({
            "title": title,
            "description": description,
            "done": False
        })

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
        return jsonify({
            "status": "error",
            "message": f"Database interaction error: {str(e)}",
            "data": None,
            "total_records": None,
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}",
            "data": None,
            "total_records": None,
        }), 500

def get_todos_service():
    try:
        data = list(mongo.db.todos.find()) 

        if not data:
            return Response(
                json_util.dumps({
                    "status": "success",
                    "message": "No todos found",
                    "data": [],
                    "total_records": None,
                }),
                mimetype="application/json",
                status=200
            )

        serialized_data = json_util.dumps({
            "status": "success",
            "message": "Todos retrieved successfully",
            "data": data,
            "total_records": len(data),
        })

        return Response(serialized_data, mimetype="application/json", status=200) 
    except PyMongoError as e:
        return jsonify({
            "status": "error",
            "message": f"Database interaction error: {str(e)}",
            "data": None,
            "total_records": None,
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}",
            "data": None,
            "total_records": None,
        }), 500


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
