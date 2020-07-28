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

@api.route('/plants/<int:id>')
def get_plant(id):
    plant = Plant.get_by_id(id)
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

@api.route('/plants/meet')
def random_plant():
    id = Plant.random_id()
    plant = Plant.get_by_id(id)
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
    plants = Plant.plant_search(search)

    if len(plants) == 0:
        results = [
            {
            'plant_image': 'https://images.unsplash.com/reserve/unsplash_529f1a3f2f5ed_1.JPG',
            'plant_type': 'Oh Crop!  We did not find any plants called {}.  Maybe try a different search term?'.format(search)
            }
        ]
    else:
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
    plant = Plant.get_by_id(plant_id)

    garden = Garden.current_garden()

    if plant.harvest_time:
        harvest_date = (datetime.now() + timedelta(days=plant.harvest_time))
        formatted_harvest_date = GardenPlant.format_time(harvest_date)
    else:
        harvest_date = None
        formatted_harvest_date = 'N/A'


    garden_plant = GardenPlant(plant_id=plant_id,plant_name=plant_name, last_watered = datetime.now(), harvest_date=harvest_date, garden_id=garden.id)
    db.session.add_all([garden_plant])
    db.session.commit()


    result = {
            'garden_plant_id': garden_plant.id,
            'plant_id': garden_plant.plant_id,
            'garden_id':garden_plant.garden_id,
            'plant_name': plant_name,
            'harvest_date': formatted_harvest_date
            }
    response = jsonify(result)
    response.status_code = 201

    return response

@api.route('/garden')
def get_garden():
    garden = Garden.current_garden()
    gardenplants = garden.gardenplants

    if len(gardenplants) == 0:
        results = {
            'info': 'You have no plants in your garden'
        }
        response = jsonify(results)
        response.status_code = 200
        return response
    else:
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

@api.route('/garden/water', methods=['PUT'])
def update_watering():
    garden_plant_id = request.args['garden_plant_id']
    garden_plant = GardenPlant.get_by_id(garden_plant_id)
    freq = garden_plant.plant.water_frequency
    raw_next_water = (datetime.now() + timedelta(days=freq))
    next_water = GardenPlant.format_time(raw_next_water)

    garden_plant.last_watered = datetime.now()
    db.session.commit()

    last_water = GardenPlant.format_time(garden_plant.last_watered)

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

@api.route('garden/plants/<int:id>', methods=['GET', 'DELETE'])
def get_gardenplant(id):
    if request.method == 'GET':
        gardenplant = GardenPlant.get_by_id(id)
        today = datetime.now()
        if gardenplant.plant.harvest_time:
            harvest = gardenplant.harvest_date
            remaining = (harvest - today).days
            formatted_harvest_date = GardenPlant.format_time(gardenplant.harvest_date)
        else:
            remaining = "N/A"
            formatted_harvest_date = "N/A"

        freq = gardenplant.plant.water_frequency
        date_of_next_water = today + timedelta(days=freq)
        days_till_water = (date_of_next_water - today).days

        formatted_date_added = GardenPlant.format_time(gardenplant.date_added)
        formatted_last_watered = GardenPlant.format_time(gardenplant.last_watered)

        result = {
            'gardenplant_id': gardenplant.id,
            'plant_name': gardenplant.plant_name,
            'date_added': formatted_date_added,
            'last_watered': formatted_last_watered,
            'harvest_date': formatted_harvest_date,
            'days_until_harvest': remaining,
            'days_until_next_water': days_till_water,
            'plant_type': gardenplant.plant.plant_type,
            'image': gardenplant.plant.image
        }
        response = jsonify(result)
        response.status_code = 200
        return response

    else:
        request.method == 'DELETE'
        gardenplant = GardenPlant.get_by_id(id)
        result = {
                    'gardenplant_id': gardenplant.id,
                    'plant_name': gardenplant.plant_name,
                }
        db.session.delete(gardenplant)
        db.session.commit()
        response = jsonify(result)
        response.status_code = 202
        return response
