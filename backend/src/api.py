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

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    print(drinks)
    drinks_list = [drink.short() for drink in drinks]
    return jsonify({
        'Sucess':True,
        'drinks': drinks_list
    }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.all()
    drinks_list = [drink.short() for drink in drinks]
    return jsonify({
        'Sucess': True,
        'drinks': drinks_list
    }), 200



'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(payload):
    data=request.get_json()
    if 'title' and 'recipe' not in data:
        abort(422)
    title=data['title']
    #https://docs.python.org/3/library/json.html
    #json.dumps from the docs solves the insert issue
    recipe = json.dumps(data['recipe'])
    new_drink = Drink(title=title,recipe=recipe)
    new_drink.insert()
    drinks_list = [new_drink.long()]
    return jsonify({
        'success':True,
        'drinks':drinks_list
    })


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
@app.route('/drinks/<int:id>',methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(payload,id):
    # get the drink by id
    drink = Drink.query.get(id)
    # if it  doesnt exist abort 422
    if not drink:
        abort(404)
    data = request.get_json()
    #make sure if title and recipe are in body then update the specified field
    if 'title' in data:
        drink.title = data['title']
    if 'recipe' in data:
        drink.recipe=json.dumps(data['recipe'])
    drink.update()
    drinks_list = [drink.long()]
    return jsonify({
        'success':True,
        'drinks':drinks_list

    })



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
@app.route('/drinks/<int:id>',methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload,id):
    #get the drink by id
    drink = Drink.query.get(id)
    #if it  doesnt exist abort 422
    if not drink:
        abort(422)
    drink.delete()
    return jsonify({
        'success':True,
        'delete':id
    })



## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "not found"
                    }), 404
'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def authentication_error(error):
    return jsonify({
                    "success": False,
                    "error": error.status_code,
                    "message": error.error['description']
                    }), error.status_code


@app.errorhandler(401)
def unaothorized(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "unauthorized"
                    }), 401
