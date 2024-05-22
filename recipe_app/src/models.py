import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# RECIPES_INGREDIENTS TABLE MODEL - (association table for many-to-many)
recipes_ingredients = db.Table(
    'recipes_ingredients',
    db.Column(
        'recipe_id', db.Integer,
        db.ForeignKey('recipes.id'),
        primary_key=True
    ),

    db.Column(
        'ingredients_id', db.Integer,
        db.ForeignKey('ingredients.id'),
        primary_key=True
    )
)

# RECIPES TABLE MODEL 
class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, unique=True, nullable=False)
    prep_time_hrs = db.Column(db.Float)
    recipe_url = db.Column(db.String, unique=True, nullable=False)
    difficulty = db.Column(db.String)
    categories = db.relationship('Category_id', backref='recipe') # Foreign Key relationship with categories (one-to-many)
    contains = db.relationship('Ingredient', secondary=recipes_ingredients, backref='contains') # Backreference is 'fake' column to connect tables

    def __init__(self, description: str, prep_time_hrs: float, recipe_url: str, difficulty: str, categories: str):
        self.description = description
        self.prep_time_hrs = prep_time_hrs
        self.recipe_url = recipe_url
        self.difficulty = difficulty
        self.categories = categories
    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'prep_time_hrs': self.prep_time_hrs,
            'recipe_url': self.recipe_url,
            'difficulty': self.difficulty,
            'category_id': self.categories,
        }

# INGREDIENTS TABLE MODEL
class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredient_name = db.Column(db.String, unique=True, nullable=False)
    in_recipes = db.relationship('Recipe', secondary=recipes_ingredients, backref='in_recipes') # Backreference is 'fake' column to connect tables

    def __init__(self, ingredient_name:str):
        self.ingredient_name = ingredient_name
    def serialize(self):
        return {
            'id': self.id,
            'ingredient_name': self.ingredient_name,
        }


# CATEGORIES TABLE MODEL
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, category_name:str):
        self.category_name = category_name
    def serialize(self):
        return {
            'id': self.id,
            'category_name': self.description,
        }