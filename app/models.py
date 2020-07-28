from . import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy import func

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
        all_plants = Plant.query.all()
        return all_plants

    def get_by_id(id):
        plant =  Plant.query.get_or_404(id)
        return plant

    def random_plant():
        plant = Plant.query.order_by(func.random()).first()
        return plant

    def plant_search(search):
        plants = db.session.query(Plant).filter(Plant.plant_type.ilike('%{}%'.format(search))).order_by(Plant.plant_type).all()
        return plants

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

    def get_by_id(id):
        gardenplant = GardenPlant.query.get_or_404(id)
        return gardenplant

    def format_time(date):
        return date.strftime("%a, %B %d, %Y")

class Garden(db.Model):
    __tablename__ = 'gardens'
    id = db.Column(db.Integer, primary_key=True)

    plants = relationship("Plant", secondary="garden_plants")
    gardenplants = relationship("GardenPlant")

    # This methods should ideally return a user's garden but for this iteration
    # of this app, we are hard coding it.

    def current_garden():
        return Garden.query.all()[0]
