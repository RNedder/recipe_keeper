from flask import Blueprint, jsonify, abort, request
from ..models import Recipe, Category, Ingredient, recipes_ingredients, db

bp = Blueprint('ingredients', __name__, url_prefix='/ingredients')


# CREATE NEW INGREDIENT - (POST)
@bp.route('', methods=['POST']) 
def create():
    # requires ingredient_name
    if 'ingredient_name' not in request.json:
        return abort(400)
    # construct Ingredient
    i = Ingredient(
        ingredient_name=request.json['ingredient_name'],
    )
    db.session.add(i) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(i.serialize())

# GET INDEX OF INGREDIENTS - (GET)
@bp.route('', methods=['GET']) # decorator 
def index():
    ingredients = Ingredient.query.all() # runs SELECT query
    result = []
    for i in ingredients:
        result.append(i.serialize()) # build list of recipes
    return jsonify(result) # return JSON response

# SHOW SPECIFIED INGREDIENT BY ID - (GET)
@bp.route('/<int:id>', methods=['GET']) # shows specified recipe by id
def show_by_id(id: int):
    i = Ingredient.query.get_or_404(id)
    return jsonify(i.serialize())

# SHOW SPECIFIED INGREDIENT BY NAME - (GET)
@bp.route('/<ingredient_name>', methods=['GET']) # shows specified recipe by id
def show_by_name(ingredient_name: str):
    i = Ingredient.query.get_or_404(id)
    return jsonify(i.serialize())

# FIND RECIPES FOR INGREDIENTS - (GET)
@bp.route('/<int:id>/in_recipes', methods=['GET'])
def in_recipes(id: int):
    i = Ingredient.query.get_or_404(id)
    result = []
    for r in i.contains:
        result.append(r.serialize())
    return jsonify(result)

# UPDATE INGREDIENT - (PATCH/PUT)
@bp.route('/<int:id>', methods=['PATCH','PUT'])
def update(id):
    i = Ingredient.query.get_or_404(id)
    if 'id' not in request.json:
        return abort(400)
    try:
        db.session.commit()
        return jsonify(i.serialize())
    # if something went wrong
    except:
        return jsonify(False)

# DELETES INGREDIENT BY ID - (DELETE)
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    i = Ingredient.query.get_or_404(id)
    try:
        db.session.delete(i) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # if something went wrong
        return jsonify(False)