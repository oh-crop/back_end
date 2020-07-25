from . import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref

class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    plant_type = db.Column(db.String(50))
    image = db.Column(db.Unicode(255))
    lighting = db.Column(db.String(50))
    water_frequency = db.Column(db.Integer)
    harvest_time = db.Column(db.Integer, nullable=True)
    root_depth = db.Column(db.Integer)
    annual = db.Column(db.String(50))

    gardens = relationship("Garden", secondary="garden_plants")

    def get_all():
        return Plant.query.all()

    def in_garden(self):
        Garden.query.filter_by(plant_id=self.id).first()

    def random_id():
        from random import randint
        num = randint(1, 24)
        return num

class GardenPlant(db.Model):
    __tablename__ = 'garden_plants'
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'))
    garden_id = db.Column(db.Integer, db.ForeignKey('gardens.id'))
    plant_name = db.Column(db.String(60))
    last_watered = db.Column(db.DateTime)
    date_added = db.Column(db.DateTime, default=datetime.now())
    harvest_date = db.Column(db.DateTime)
    
    plant = relationship("Plant")

class Garden(db.Model):
    __tablename__ = 'gardens'
    id = db.Column(db.Integer, primary_key=True)

    plants = relationship("Plant", secondary="garden_plants")
    gardenplants = relationship("GardenPlant")
