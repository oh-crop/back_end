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

    def test_it_has_a_plant_type(self):
        plant = Plant(plant_type='Celery')
        garden_plant = GardenPlant(plant_id=plant.id)
        self.assertTrue(garden_plant.plant_id == plant.id)

if __name__ == "__main__":
    unittest.main()
