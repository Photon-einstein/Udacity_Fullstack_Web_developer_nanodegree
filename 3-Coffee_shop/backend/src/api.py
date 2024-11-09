import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin",
                         "*")  # Allow all origins
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this functon will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks", methods=['GET'])
def get_drinks():
    try:
        drinks_bulk = Drink.query.order_by(Drink.id).all()
        if len(drinks_bulk) == 0:
            abort(404)
        drinks = {}
        for entry in drinks_bulk:
            drinks.update(entry.short())
        return jsonify(
            {
                "success": True,
                "drinks": drinks
            }
        )
    except ValueError:
        # Handle specific error for invalid data types
        abort(404)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks-detail", methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    try:
        drinks_bulk = Drink.query.order_by(Drink.id).all()
        if len(drinks_bulk) == 0:
            abort(404)
        drinks = []
        for entry in drinks_bulk:
            drinks.append(entry.long())
        return jsonify(
            {
                "success": True,
                "drinks": drinks
            }
        )
    except Exception as e:
        print(f"Error: {e}")
        abort(404)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=["POST"])
@requires_auth('post:drinks')
def create_drinks(jwt):
    body = request.get_json()
    print("Received body:", body)
    try:
        new_title = body.get("title", None)
        new_recipe = json.dumps(body.get("recipe", None))
        if not new_title or not new_recipe:
            abort(422)
        # Convert the recipe to a JSON string if it's a list
        if isinstance(new_recipe, list):
            new_recipe = json.dumps(new_recipe)
        drink = Drink(title=new_title,
                      recipe=new_recipe)
        drink.insert()
        return jsonify(
            {
                "success": True,
                "drinks": drink.long()
            }
        )
    except Exception as e:
        print(f"Error: {e}")
        abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    body = request.get_json()
    try:
        drink_to_patch = Drink.query.filter(Drink.id == id).one_or_none()
        if drink_to_patch is None:
            abort(404)
        title = body.get("title")
        recipe = body.get("recipe")

        # update the field if data is available
        if title:
            drink_to_patch.title = title
        if recipe:
            drink_to_patch.recipe = json.dumps(recipe)

        drink_to_patch.update()

        return jsonify(
            {
                "success": True,
                "drinks": [drink_to_patch.long()]
            }
        ), 200
    except Exception as e:
        print(e)
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<int:drink_id>", methods=["DELETE"])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    try:
        drink = Drink.query.filter(
            Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404)
        drink.delete()
        return jsonify(
            {
                "success": True,
                "delete": drink_id
            }
        ), 200
    except Exception as e:
        print(e)
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(400)
def bad_request(error):
    return (
        jsonify({"success": False, "error": 400,
                "message": "bad request"}),
        400,
    )


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404,
                "message": "resource not found"}),
        404,
    )


@app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422,
                "message": "unprocessable"}),
        422,
    )


@app.errorhandler(500)
def internal_server_error(error):
    return (
        jsonify({"success": False, "error": 500,
                "message": "internal server error"}),
        500,
    )


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
