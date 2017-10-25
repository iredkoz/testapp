# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, flash,url_for, jsonify, app
from . import recipeapp
import os
import simplejson as json
import datetime
import wtforms_json
from forms import IngridientForm, StepForm, RecipeForm
from .. import db
from ..models import Recipes, Ingridients, Steps, StepPhotos, RecipePhotos,IngidientList, Photos
#from ..models import RecipesSchema, IngridientsSchema, StepsSchema, StepsPhotosSchema, RecipePhotosSchema, IngridientListSchema
from werkzeug.utils import secure_filename
import constants
import logging
import logging.handlers

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler('/var/uploads/flask.log', maxBytes=300000, backupCount=2)
logger.addHandler(handler)
logging.debug('started blueprint')

UPLOAD_FOLDER = '/var/uploads/'

@recipeapp.route('/recipes')
def recipes_main():
    recipes = Recipes.query.order_by(Recipes.name).all()
    return render_template('recipeapp/recipeapp.html',cats=constants.categories, recipes=recipes)

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
    if form.validate_on_submit():
        recipe = Recipes(name=form.name.data,note=form.description.data, category=form.category.data, subcategory=form.subcategory.data, food_type=form.cuisine.data,prep_time=form.prep_time.data,favourite=form.favourite)
        db.session.add(recipe)        
        db.session.flush()
        for p in form.photos.entries:
            photo = Photos.query.filter_by(filename=p.data).first()
            if photo:
                p_list = RecipePhotos(recipe_id=recipe.id,photo_id=photo.id)
                db.session.add(p_list)
                db.session.flush()
            
        for i in form.ingridients.entries:
            i_list = IngidientList(recipe_id=recipe.id,quantity = i.data['quantity'], unit = i.data['unit'], ingridient_id=i.data['name'].id)
            db.session.add(i_list)
            db.session.flush()
            
        for s in form.steps.entries:
            s_list = Steps(description = s.data['description'], recipe_id=recipe.id)
            db.session.add(s_list)
            db.session.flush()
            logging.debug(s.data['photo'])
            photo = Photos.query.filter_by(filename=s.data['photo']).first()
            
            if photo:
                s_photo = StepPhotos(step_id = s_list.id, photo_id=photo.id)
                db.session.add(s_photo)
                db.session.flush()
        db.session.commit()
        flash('Recipe added successfully!','alert-success')
        return redirect(url_for('recipeapp.new_recipe'))
    if form.errors:
        flash(form.errors,'alert-danger')
    return render_template('recipeapp/editor.html',form=form)

@recipeapp.route('/upload-photo',methods = ['GET','POST'])
def upload_photo():
    if request.method=='POST':
        f=request.files['file']
        if not Photos.query.filter_by(filename=f.filename).first():
            f.save(os.path.join(UPLOAD_FOLDER, f.filename))
            photo = Photos(filename=f.filename)
            db.session.add(photo)
            db.session.commit()
    return ('',204)

