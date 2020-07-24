from flask import jsonify, request, current_app, url_for
from . import api
from ..models import Plant
from flask_sqlalchemy import SQLAlchemy
from app import db

@api.route('/')
def endpoint():
    return "I need to go take a shower so I can't tell if I'm crying or not."

@api.route('/plants/<int:id>')
def get_plant(id):
    plant = Plant.query.get_or_404(id)
    result = {
                'id': plant.id,
                'plant_type': plant.plant_type,
                'plant_image': plant.image,
                'lighting': plant.lighting,
                'days_between_water': plant.water_frequency,
                'days_to_harvest_from_seed': plant.harvest_time,
                'root_depth_in': plant.root_depth,
                'annual?': plant.annual
                }
    response = jsonify(result)
    response.status_code = 200
    return response

@api.route('/plants/')
def all_plants():
    plants = Plant.get_all()
    results = []

    for plant in plants:
        obj = {
            'id': plant.id,
            'name': plant.name
        }
        results.append(obj)
    response = jsonify(results)
    response.status_code = 200
    return response

@api.route('/plants/meet')
def random_plant():
    id = Plant.random_id()
    plant = Plant.query.get_or_404(id)
    result = {
                'id': plant.id,
                'plant_type': plant.plant_type,
                'plant_image': plant.image
                }
    response = jsonify(result)
    response.status_code = 200
    return response

@api.route('/plants/search')
def search_plants():
    search = request.args['q']
    plants = db.session.query(Plant).filter(Plant.plant_type.ilike('%{}%'.format(search))).all()
    results = []

    for plant in plants:
        obj = {
            'plant_type': plant.plant_type,
            'plant_image': plant.image,
        }
        results.append(obj)
    response = jsonify(results)
    response.status_code = 200
    return response
