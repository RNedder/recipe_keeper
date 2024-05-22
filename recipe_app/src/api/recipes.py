from flask import Blueprint, jsonify, abort, request
from ..models import Recipe, Category, Ingredient, recipes_ingredients, db

bp = Blueprint('recipes', __name__, url_prefix='/recipes')


# CREATE NEW RECIPE - (POST)
@bp.route('', methods=['POST']) 
def create():
    # requires description and recipe_url
    if 'description' not in request.json or 'recipe_url' not in request.json:
        return abort(400)
    # construct Recipe
    r = Recipe(
        description=request.json['description'],
        prep_time_hrs=request.json['prep_time_hrs'],
        recipe_url=request.json['recipe_url'],
        difficulty=request.json['difficulty'],
        category_id=request.json['category_id']
    )
    db.session.add(r) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(r.serialize())

# GET INDEX OF RECIPES - (GET)
@bp.route('', methods=['GET']) # decorator 
def index():
    recipes = Recipe.query.all() # runs SELECT query
    result = []
    for r in recipes:
        result.append(r.serialize()) # build list of recipes
    return jsonify(result) # return JSON response

# SHOW SPECIFIED RECIPE BY ID - (GET)
@bp.route('/<int:id>', methods=['GET']) # shows specified recipe by id
def show_by_id(id: int):
    r = Recipe.query.get_or_404(id)
    return jsonify(r.serialize())

# SHOW SPECIFIED RECIPE BY NAME - (GET)
@bp.route('/<description>', methods=['GET']) # shows specified recipe by id
def show_by_name(description: str):
    i = Ingredient.query.get_or_404(id)
    return jsonify(i.serialize())

# FIND RECIPE INGREDIENTS - (GET)
@bp.route('/<int:id>/contains', methods=['GET'])
def contains(id: int):
    r = Recipe.query.get_or_404(id)
    result = []
    for i in r.contains:
        result.append(i.serialize())
    return jsonify(result)

# UPDATE RECIPE - (PATCH/PUT)
@bp.route('/<int:id>', methods=['PATCH','PUT'])
def update(id):
    r = Recipe.query.get_or_404(id)
    if 'id' not in request.json:
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
    r = Recipe.query.get_or_404(id)
    try:
        db.session.delete(r) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # if something went wrong
        return jsonify(False)



