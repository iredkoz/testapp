# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, flash,url_for, jsonify
from . import recipeapp

import simplejson as json
import datetime
from forms import IngridientForm, StepForm, RecipeForm
from .. import db
from ..models import Recipes, Ingridients, Steps, StepPhotos, RecipePhotos,IngidientList
#from ..models import RecipesSchema, IngridientsSchema, StepsSchema, StepsPhotosSchema, RecipePhotosSchema, IngridientListSchema

import constants


@recipeapp.route('/recipes')
def recipes_main():
    return render_template('recipeapp/recipeapp.html',cats=constants.categories)

@recipeapp.route('/recipes/<cat>')
def category(cat):
    items = Recipes.query.filter_by(category=cat).all()
    return render_template('recipeapp/category.html',cat=cat)

@recipeapp.route('/recipes/<int:recipe_id>')
def show_recipe(recipe_id):
    recipe = Recipes.query.get(recipe_id)
    steps = Steps.query.filter_by(recipe = recipe).all()
    return render_template('recipeapp/recipe.html',recipe=recipe,steps=steps)

@recipeapp.route('/new-ingridient',methods = ['GET','POST'])
def new_ingridient():
    itemForm=IngridientForm()
    if itemForm.validate_on_submit():
        if Ingridients.query.filter_by(name=itemForm.name.data).first():
            flash('Item already exists!','alert-danger')
        else:
            item = Ingridients(name=itemForm.name.data, note = itemForm.note.data, category=itemForm.cat.data)
            db.session.add(item)
            db.session.commit()
            flash('Item added successfully!','alert-success')
    return render_template('recipeapp/editor.html',itemForm=itemForm)

@recipeapp.route('/new-recipe',methods = ['GET','POST'])
def new_recipe():
    form = RecipeForm()
    return render_template('recipeapp/editor.html',form=form)