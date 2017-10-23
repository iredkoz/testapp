# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from flask.ext.uploads import UploadSet, IMAGES
from wtforms.fields import *
from wtforms.validators import *
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from ..models import Recipes, Ingridients, Steps, StepPhotos, RecipePhotos,IngidientList
import constants
import wtforms_json

images = UploadSet('images',IMAGES)
wtforms_json.init()

def query_ingridients():
    return Ingridients.query

class IngridientForm(FlaskForm):
    name = StringField('Ingridient Name',validators = [DataRequired('Please enter ingridient name')], render_kw={"placeholder":"Flour, oil, salt..","class":"form-control"})
    note = TextAreaField('Product Note', render_kw={"placeholder":"Notes..","class":"form-control"})
    cat = SelectField('Category', choices=[(item,item) for item in constants.food_cats],render_kw={"class":"form-control"})

class StepForm(FlaskForm):
    description = TextAreaField('Description',render_kw={"placeholder":"What to do..","class":"form-control"})    
    photo = HiddenField('Photo-1',render_kw={"class":"step-photo"})
    
class RecipeIngridientForm(FlaskForm):
    name = QuerySelectField('Ingridient',query_factory=query_ingridients,  get_label='name',allow_blank=False, render_kw={"class":"form-control select-ingridient col-3"})
    quantity = IntegerField('Quantity',default=0,render_kw={"class":"form-control col-2"})
    unit = SelectField('Units',choices=[(item,item) for item in constants.units],render_kw={"class":"form-control col-2"})

class RecipeForm(FlaskForm):
    name = StringField('Recepie', render_kw={"class":"form-control"})
    category = SelectField('Category', choices=[(item,item) for item in constants.categories],render_kw={"class":"form-control"})
    subcategory = SelectField('Sub-category', choices=[(item,item) for item in constants.subcategories],render_kw={"class":"form-control"})
    cuisine = SelectField('Cuisine', choices=[(item,item) for item in constants.cuisine],render_kw={"class":"form-control"})
    description = TextAreaField('Recipe description', render_kw={"placeholder":"Description..","class":"form-control"})
    prep_time =IntegerField('Cooking time',render_kw={"class":"form-control duration-picker"})
    favourite = BooleanField('Favourite',render_kw={"class":"form-check-input"})
    
    ingridients = FieldList(FormField(RecipeIngridientForm,render_kw={"class":"form-group"}),min_entries=1)
    steps = FieldList(FormField(StepForm, render_kw={"class":"form-group"}),min_entries=1)
    #step = TextAreaField('Description',render_kw={"placeholder":"What to do..","class":"form-control"})
    #photo = HiddenField('Photo-1',render_kw={"class":"step-photo"})
    
    