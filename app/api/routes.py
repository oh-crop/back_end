from flask import jsonify, request, current_app, url_for
from ..models import Plant, Garden, GardenPlant
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
from app import db
from . import api
# Base endpoint test used when testing deployment.
# Also used later as a motivational message.


@api.route('/')
def endpoint():
    """Return a simple motivational message when app is deployed."""
    return "I need to go take a shower so I can't tell if I'm crying or not."


@api.route('/plants/')
def all_plants():
    """Return all plant objects."""
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
    """
    Return a given plant when given its ID.

    :param id: The ID of the plant will be passed in as an int.
    :return: A JSON response will be generated including a status code of 200
        if a plant is found with the given ID.
    """
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
    """Return a random plant from the database."""
    plant = Plant.random_plant()
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
    """
    Return a plant from the database based on search criteria.

    This request will be sent in with search params which will then be passed
        into the plant_search() method.  If no plants are found in the search,
        a message is sent to the user with that information.

    :return: A JSON response with plants found relating to the search.
    """
    search = request.args['q']
    plants = Plant.plant_search(search)

    if len(plants) == 0:
        results = [
            {'plant_image':
                'https://'
                'images.unsplash.com/reserve/unsplash_529f1a3f2f5ed_1.JPG',
             'plant_type':
                'Oh Crop!  We did not find any plants called {}.  '
                'Maybe try a different search term?'.format(search)}
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


@api.route('/garden')
def get_garden():
    """
    Return all the plants in the current garden (gardenplants).

    If garden has no plants, a message will be displayed saying so.

    :return: JSON response with all plant objects that are in the current
        garden.
    """
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


@api.route('/garden', methods=['POST'])
def add_to_garden():
    """
    Add a plant that exists in the database to the current garden.

    POST request will include query params of plant_id and plant_name.
        plant_id is the ID of the type of plant in the DB.
        plant_name is the given name of the plant to identify it in your
            garden.  (Example: plant_name = 'Travis', plant_id='12' will
            add whatever plant has ID 12 to the garden and will be called
            Travis for identification purposes.)

    :return: JSON response with information about the plant added.
    """
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

    garden_plant = GardenPlant(plant_id=plant_id,
                               plant_name=plant_name,
                               last_watered=datetime.now(),
                               harvest_date=harvest_date,
                               garden_id=garden.id)
    db.session.add_all([garden_plant])
    db.session.commit()

    result = {
            'garden_plant_id': garden_plant.id,
            'plant_id': garden_plant.plant_id,
            'garden_id': garden_plant.garden_id,
            'plant_name': plant_name,
            'harvest_date': formatted_harvest_date
        }

    response = jsonify(result)
    response.status_code = 201

    return response


@api.route('/garden/water', methods=['PUT'])
def update_watering():
    """
    Water a gardenplant.

    This request will take a gardenplant ID as a query param and update
        its watering information.  It will update when the plant was watered
        and then calculate when it will need to be watered again.

    :return: JSON response including updated watering information on the plant.
    """
    garden_plant_id = request.args['garden_plant_id']
    garden_plant = GardenPlant.get_by_id(garden_plant_id)
    freq = garden_plant.plant.water_frequency
    raw_next_water = (garden_plant.last_watered + timedelta(freq))
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
    """
    Get information about a plant or delete it from the garden.

    GET request will return profile information about the plant.
    :return: JSON response with all important plant profile info.

    DELETE request will remove the gardenplant from the current garden.
    :return: JSON response with ID and name of removed plant.
    """
    if request.method == 'GET':
        gardenplant = GardenPlant.get_by_id(id)
        today = datetime.now()
        if gardenplant.plant.harvest_time:
            harvest = gardenplant.harvest_date
            remaining = (harvest - today).days
            formatted_harvest_date = GardenPlant.format_time(
                gardenplant.harvest_date)
        else:
            remaining = "N/A"
            formatted_harvest_date = "N/A"

        freq = gardenplant.plant.water_frequency
        date_of_next_water = gardenplant.last_watered + timedelta(freq)
        days_till_water = (date_of_next_water - today).days

        formatted_date_added = GardenPlant.format_time(gardenplant.date_added)
        formatted_last_watered = GardenPlant.format_time(
            gardenplant.last_watered)

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
