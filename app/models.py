from . import db
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

    def get_all():
        return Plant.query.all()

    def get_one(id):
        return Plant.query.filter_by(id=id).first()
