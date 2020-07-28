import unittest
import os
import json
from app import create_app, db
from app.models import Plant, GardenPlant, Garden
from datetime import timedelta
import datetime

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

# Plant Model Tests

    def test_a_plant_has_attributes(self):
        agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
        db.session.add_all([agatha])
        db.session.commit()
        self.assertTrue(type(agatha.id) is int)
        self.assertEqual(agatha.plant_type, 'Roma Tomato')
        self.assertEqual(agatha.image, 'agatha_photo.jpg')
        self.assertEqual(agatha.lighting, 'Full Sun')
        self.assertEqual(agatha.water_frequency, 2)
        self.assertEqual(agatha.harvest_time, 60)
        self.assertEqual(agatha.root_depth, 12)
        self.assertEqual(agatha.annual, "Annual")

    def test_it_can_retrieve_all_plants(self):
        zeke = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
        db.session.add_all([zeke, dan, agatha])
        db.session.commit()

        plants = Plant.get_all()

        self.assertIn(zeke, plants)
        self.assertIn(dan, plants)
        self.assertIn(agatha, plants)

    def test_it_can_get_a_plant_by_id(self):
        zeke = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
        db.session.add_all([zeke, dan, agatha])
        db.session.commit()

        plant = Plant.get_by_id(zeke.id)

        self.assertEqual(zeke.id, plant.id)
        self.assertNotEqual(dan.id, plant.id)
        self.assertNotEqual(agatha.id, plant.id)

    def test_a_plant_can_get_a_random_plant(self):
        zeke = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
        db.session.add_all([zeke, dan, agatha])
        db.session.commit()

        plant = Plant.random_plant()

        ids = [zeke.id, dan.id, agatha.id]
        self.assertIn(plant.id, ids)
        self.assertIsNotNone(plant.plant_type)
        self.assertIsNotNone(plant.image)
        self.assertIsNotNone(plant.lighting)
        self.assertIsNotNone(plant.water_frequency)
        self.assertIsNotNone(plant.root_depth)
        self.assertIsNotNone(plant.annual)
        self.assertTrue(type(plant) == Plant)
        self.assertFalse(type(plant) == Garden)
        self.assertFalse(type(plant) == GardenPlant)


    def test_seach_for_a_plant(self):
        zeke = Plant(plant_type='Cherry Tomato',image='jim_photo.jpg',lighting='Full Sun',water_frequency=3,harvest_time=50,root_depth=12,annual="Annual")
        dan = Plant(plant_type='Cactus',image='cactus_dan.jpg',lighting='Full Sun',water_frequency=7,harvest_time=None,root_depth=8,annual="Annual")
        agatha = Plant(plant_type='Roma Tomato',image='agatha_photo.jpg',lighting='Full Sun',water_frequency=2,harvest_time=60,root_depth=12,annual="Annual")
        db.session.add_all([zeke, dan, agatha])
        db.session.commit()

        results = Plant.plant_search('cactus')
        self.assertEqual(1, len(results))

        cactus_dan = results[0]

        self.assertEqual(dan.id, cactus_dan.id)
        self.assertNotEqual(zeke.id, cactus_dan.id)
        self.assertNotEqual(agatha.id, cactus_dan.id)

# Garden Plant Model Tests
    def test_a_gardenplant_has_attributes(self):
        date = datetime.date(2013,1,1)
        garden_plant = GardenPlant(plant_id=1,garden_id=2,plant_name="Wile E. Coyote",last_watered=date,date_added=date,harvest_date=date)

        self.assertEqual(garden_plant.plant_id, 1)
        self.assertEqual(garden_plant.garden_id, 2)
        self.assertEqual(garden_plant.plant_name, "Wile E. Coyote")
        self.assertEqual(garden_plant.last_watered, date)
        self.assertEqual(garden_plant.date_added, date)
        self.assertEqual(garden_plant.harvest_date, date)

    def test_it_can_get_a_gardenplant_by_id(self):
        tom_garden_plant = GardenPlant(plant_name="Tom")
        jerry_garden_plant = GardenPlant(plant_name="Jerry")
        db.session.add_all([tom_garden_plant, jerry_garden_plant])
        db.session.commit()

        garden_plant_obj = GardenPlant.get_by_id(tom_garden_plant.id)

        self.assertEqual(garden_plant_obj.id, tom_garden_plant.id)
        self.assertEqual(garden_plant_obj.plant_name, "Tom")
        self.assertNotEqual(garden_plant_obj.id, jerry_garden_plant.id)
        self.assertNotEqual(garden_plant_obj.plant_name, "Jerry")

    def test_it_can_format_time(self):
        date = datetime.date(2013,1,1)

        formatted_date_time = GardenPlant.format_time(date)
        self.assertEqual("Tue, January 01, 2013", formatted_date_time)

# Garden Model Tests
    def test_a_garden_has_attributes(self):
        garden = Garden(id=1)

        self.assertTrue(type(garden.id) is int)
