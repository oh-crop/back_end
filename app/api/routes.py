from flask import jsonify, request, current_app, url_for
from . import api
from ..models import Plant, Garden, GardenPlant
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
                'lifecycle': plant.annual
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

@api.route('/garden', methods=['POST'])
def add_to_garden():
    plant_id = request.args['plant_id']
    plant_name = request.args['plant_name']
    plant = Plant.query.filter_by(id=plant_id,).first()
    garden = Garden.query.all()[0]

    if plant.harvest_time:
        harvest_date = (datetime.now() + timedelta(days=plant.harvest_time))
        days_to_harvest = harvest_date.strftime("%a, %B %d %Y")
    else:
        days_to_harvest = None


    garden_plant = GardenPlant(plant_id=plant_id,plant_name=plant_name, harvest_date=days_to_harvest,garden_id=garden.id)
    db.session.add_all([garden_plant])
    db.session.commit()


    result = {
    'garden_plant_id': garden_plant.id,
    'plant_id': garden_plant.plant_id,
    'garden_id':garden_plant.garden_id,
    'plant_name': plant_name,
    'harvest_date':garden_plant.harvest_date
    }
    response = jsonify(result)
    response.status_code = 201

    return response

@api.route('/garden')
def get_garden():
    garden = Garden.query.all()[0]
    gardenplants =  garden.gardenplants

    results = []

    for plant in gardenplants:
        obj = {
            'id': plant.id,
            'plant_name': plant.plant_name,
        }
        results.append(obj)
    response = jsonify(results)
    response.status_code = 200
    return response

@api.route('/garden/water', methods=['POST'])
def update_watering():
    garden_plant_id = request.args['garden_plant_id']
    garden_plant = GardenPlant.query.get_or_404(garden_plant_id)
    freq = garden_plant.plant.water_frequency
    raw_next_water = (datetime.now() + timedelta(days=freq))
    next_water = raw_next_water.strftime("%a, %B %d %Y")

    garden_plant.last_watered = datetime.now()
    db.session.commit()

    last_water = garden_plant.last_watered.strftime("%a, %B %d %Y")

    results = {
        'id': garden_plant.id,
        'name': garden_plant.plant_name,
        'plant_type': garden_plant.plant.plant_type,
        'water_frequency': freq,
        'last_watered': last_water,
        'next_water': next_water
    }
    response = jsonify(results)
    response.status_code = 201
    return response

@api.route('garden/plants/<int:id>')
def get_gardenplant(id):
    gardenplant = GardenPlant.query.get_or_404(id)
    result = {
        'id': gardenplant.id,
        'plant_name': gardenplant.plant_name,
        'date_added': gardenplant.date_added,
        'last_watered': gardenplant.last_watered,
        'harvest_date': gardenplant.harvest_date,
        'plant_type': gardenplant.plant.plant_type
    }
    # code.interact(local=dict(globals(), **locals()))
    response = jsonify(result)
    response.status_code = 200
    return response
