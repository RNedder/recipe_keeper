from flask import Blueprint, jsonify, abort, request
from ..models import Recipe, Category, Ingredient, recipes_ingredients, db

bp = Blueprint('categories', __name__, url_prefix='/categories')


# CREATE NEW CATEGORY - (POST)
@bp.route('', methods=['POST']) 
def create():
    # requires description and recipe_url
    if 'category_name' not in request.json:
        return abort(400)
    # construct Recipe
    c = Category(
        category_name=request.json['category_name']
    )
    db.session.add(c) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(c.serialize())

# GET INDEX OF CATEGORIES - (GET)
@bp.route('', methods=['GET']) # decorator 
def index():
    categories = Category.query.all() # runs SELECT query
    result = []
    for c in categories:
        result.append(c.serialize()) # build list of recipes
    return jsonify(result) # return JSON response

# UPDATE CATEGORY - (PATCH/PUT)
@bp.route('/<int:id>', methods=['PATCH','PUT'])
def update(id):
    r = Recipe.query.get_or_404(id)
    if 'id' not in request.json or 'category_name' not in request.json:
        return abort(400)
    try:
        db.session.commit()
        return jsonify(r.serialize())
    # if something went wrong
    except:
        return jsonify(False)

# DELETES RECIPE BY ID - (DELETE)
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    c = Category.query.get_or_404(id)
    try:
        db.session.delete(c) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # if something went wrong
        return jsonify(False)



