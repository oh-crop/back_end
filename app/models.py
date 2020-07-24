from . import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    plant_type = db.Column(db.String(50))
    image = db.Column(db.Unicode(255))
    lighting = db.Column(db.String(50))
    water_frequency = db.Column(db.Integer)
    harvest_time = db.Column(db.Integer, nullable=True)
    root_depth = db.Column(db.Integer)
    annual = db.Column(db.Boolean)

    def in_garden(self):
        Garden.query.filter_by(plant_id=self.id).first()

class Garden(db.Model):
    __tablename__ = 'gardens'
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, ForeignKey('plants.id'))
    plant_name = db.Column(db.String(60))
    last_watered = db.Column(db.DateTime)
    date_added = db.Column(db.DateTime, default=datetime.now())
