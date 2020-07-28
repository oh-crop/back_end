import unittest
import os
import json
from app import create_app, db
from app.models import Plant, GardenPlant

class ModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_it_has_a_plant_type(self):
        plant = Plant(plant_type='Celery')
        self.assertTrue(plant.plant_type == 'Celery')
        self.assertTrue(plant.plant_type != 'Corn')

    def test_it_can_retrieve_all_plants(self):
        zeke = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
        db.session.add_all([zeke, dan, agatha])
        db.session.commit()

        plants = Plant.query.all()

        self.assertIn(zeke, plants)
        self.assertIn(dan, plants)
        self.assertIn(agatha, plants)

    def test_it_has_a_gardenplant(self):
        plant = Plant(plant_type='Celery')
        garden_plant = GardenPlant(plant_id=plant.id)
        self.assertTrue(garden_plant.plant_id == plant.id)
