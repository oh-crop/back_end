from . import db

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
