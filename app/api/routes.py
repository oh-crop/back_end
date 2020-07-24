from flask import jsonify, request, current_app, url_for
from . import api
from ..models import Plant
from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import datetime
from datetime import timedelta

some_engine = create_engine('postgresql://localhost/oh_crop')
Session = sessionmaker(bind=some_engine)
session = Session()


@api.route('/')
def endpoint():
    return "I need to go take a shower so I can't tell if I'm crying or not."

@api.route('/plants/<int:id>')
def get_plant(id):
    plant = Plant.query.filter_by(id=id).first()
    result = {
                'id': plant.id,
                'name': plant.name,
                'plant_type': plant.plant_type
                }
    response = jsonify(result)
    response.status_code = 200
    return response

@api.route('/garden/plants', methods=['POST'])
def add_to_garden(id):
    plant_id = request.args['plant_id']
    plant_name = request.args['plant_name']

    plant = Plant.query.filter_by(id=plant_id).first()

    garden = Garden(plant_id=plant_id)
    garden.save()

    days_to_harvest = (datetime.now() + timedelta(days=1))

    response = jsonify({
        'id': garden.id,
        'plant_name': plant_name,
        'last_watered': datetime.now(),
        'plant_type': plant.plant_type,
        'lighting': plant.lighting,
        'root_depth_inches': plant.root_depth,
        'days_between_water': plant.water_frequency,
        'annual?': plant.annual,
        'days_to_harvest':days_to_harvest
    })
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
    from random import randint
    id = randint(1, 24)
    plant = Plant.query.filter_by(id=id).first()
    result = {
                'id': plant.id,
                'name': plant.name,
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
