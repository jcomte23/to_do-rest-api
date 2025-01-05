from bson import ObjectId, json_util
from flask import Response, jsonify, request
from src.config.mongodb import mongo
from pymongo.errors import PyMongoError


def create_todo_service():
    try:
        data = request.get_json()

        if not data:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "The request body is empty",
                        "data": None,
                        "total_records": None,
                    }
                ),
                400,
            )

        title = data.get("title")
        if not title:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "The 'title' field is required",
                        "data": None,
                        "total_records": None,
                    }
                ),
                400,
            )

        description = data.get("description", None)

        response = mongo.db.todos.insert_one(
            {"title": title, "description": description, "done": False}
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Todo created successfully",
                    "data": {
                        "id": str(response.inserted_id),
                        "title": title,
                        "description": description,
                        "done": False,
                    },
                }
            ),
            201,
        )
    except PyMongoError as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Database interaction error: {str(e)}",
                    "data": None,
                    "total_records": None,
                }
            ),
            500,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An unexpected error occurred: {str(e)}",
                    "data": None,
                    "total_records": None,
                }
            ),
            500,
        )


def get_todos_service():
    try:
        data = list(mongo.db.todos.find())

        if not data:
            return Response(
                json_util.dumps(
                    {
                        "status": "success",
                        "message": "No todos found",
                        "data": [],
                        "total_records": None,
                    }
                ),
                mimetype="application/json",
                status=200,
            )

        serialized_data = json_util.dumps(
            {
                "status": "success",
                "message": "Todos retrieved successfully",
                "data": data,
                "total_records": len(data),
            }
        )

        return Response(serialized_data, mimetype="application/json", status=200)
    except PyMongoError as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Database interaction error: {str(e)}",
                    "data": None,
                    "total_records": None,
                }
            ),
            500,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An unexpected error occurred: {str(e)}",
                    "data": None,
                    "total_records": None,
                }
            ),
            500,
        )


def get_todo_service(id):
    try:
        if not ObjectId.is_valid(id):
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Invalid ID format",
                        "data": None,
                        "total_records": None,
                    }
                ),
                400,
            )

        data = mongo.db.todos.find_one({"_id": ObjectId(id)})

        if not data:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "ToDo not found",
                        "data": None,
                        "total_records": None,
                    }
                ),
                404,
            )

        serialized_data = json_util.dumps(
            {
                "status": "success",
                "message": "ToDo retrieved successfully",
                "data": data,
                "total_records": len(data),
            }
        )

        return Response(serialized_data, mimetype="application/json", status=200)
    except PyMongoError as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Database interaction error: {str(e)}",
                    "data": None,
                    "total_records": None,
                }
            ),
            500,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An unexpected error occurred: {str(e)}",
                    "data": None,
                    "total_records": None,
                }
            ),
            500,
        )


def update_todo_service(id):
    try:
        if not ObjectId.is_valid(id):
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Invalid ID format",
                        "data": None,
                        "total_records": None,
                    }
                ),
                400,
            )

        data = request.get_json()

        if not data or not isinstance(data, dict):
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "The request body must contain valid JSON",
                        "data": None,
                        "total_records": None,
                    }
                ),
                400,
            )

        response = mongo.db.todos.update_one({"_id": ObjectId(id)}, {"$set": data})

        if response.matched_count == 0:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Todo not found",
                        "data": None,
                        "total_records": None,
                    }
                ),
                404,
            )

        if response.modified_count == 0:
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "No changes made to the Todo",
                        "data": None,
                        "total_records": None,
                    }
                ),
                200,
            )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Todo updated successfully",
                    "data": None,
                    "total_records": None,
                }
            ),
            200,
        )
    except PyMongoError as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Database interaction error: {str(e)}",
                    "data": None,
                    "total_records": None,
                }
            ),
            500,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"An unexpected error occurred: {str(e)}",
                    "data": None,
                    "total_records": None,
                }
            ),
            500,
        )


def delete_todo_service(id):
    response = mongo.db.todos.delete_one({"_id": ObjectId(id)})

    if response.deleted_count >= 1:
        return "Todo deleted successfully", 200
