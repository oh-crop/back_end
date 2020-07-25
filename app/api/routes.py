from flask import jsonify, request, current_app, url_for
from . import api
from ..models import Plant, Garden
from flask_sqlalchemy import SQLAlchemy
from app import db
import code
from datetime import datetime
from datetime import timedelta

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
                'annual': plant.annual
                }
    response = jsonify(result)
    response.status_code = 200
    return response

@api.route('/garden', methods=['POST'])
def add_to_garden():
    plant_id = request.args['plant_id']
    plant_name = request.args['plant_name']
    plant = Plant.query.filter_by(id=plant_id,).first()

    if plant.harvest_time:
        harvest_date = (datetime.now() + timedelta(days=plant.harvest_time))
        days_to_harvest = harvest_date.strftime("%a, %B %d %Y")
    else:
        days_to_harvest = None


    garden = Garden(plant_id=plant_id,plant_name=plant_name, harvest_date=days_to_harvest)
    db.session.add_all([garden])
    db.session.commit()


    result = {
        'plant_id': garden.plant_id,
        'plant_name': plant_name,
        'harvest_date':garden.harvest_date
    }
    response = jsonify(result)
    response.status_code = 201
    return response

@api.route('/plants/')
def all_plants():
    plants = Plant.get_all()
    results = []

    for plant in plants:
        obj = {
            'id': plant.id,
            'image': plant.image
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
            'id': plant.id,
            'plant_type': plant.plant_type,
            'plant_image': plant.image,
        }
        results.append(obj)
    response = jsonify(results)
    response.status_code = 200
    return response
