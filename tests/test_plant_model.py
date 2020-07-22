import unittest
import os
import json
from app import create_app, db
from app.models import Plant

class PlantModelTestCase(unittest.TestCase):

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

    def test_it_has_a_name(self):
        plant = Plant(name='Gerald', plant_type='Celery')
        self.assertTrue(plant.name == 'Gerald')
        self.assertFalse(plant.name == 'Fred')
        self.assertTrue(plant.plant_type == 'Celery')
        self.assertTrue(plant.plant_type != 'Corn')

if __name__ == "__main__":
    unittest.main()
