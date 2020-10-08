from . import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy import func


class Plant(db.Model):
    """Plant model from postgresql DB."""

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
        """Return all plants in the database."""
        all_plants = Plant.query.all()
        return all_plants

    def get_by_id(id):
        """
        Return a plant by its ID.

        :param id: Integer, the ID of the plant.
        :return: The plant with the provided ID.
        """
        plant = Plant.query.get_or_404(id)
        return plant

    def random_plant():
        """Mix up plants and randomly return the first one."""
        plant = Plant.query.order_by(func.random()).first()
        return plant

    def plant_search(search):
        """
        Return a plant by search criteria.

        :param search: A string used to create a search term.
        :return: A list of all plants with that term included.  If no plants
            are found in the search an empty list is returned.
        """
        plants = db.session.query(Plant).filter(
            Plant.plant_type.ilike('%{}%'.format(search))).order_by(
                Plant.plant_type).all()
        return plants


class GardenPlant(db.Model):
    """
    Gardenplant model from PSQL database.

    A gardenplant is a joins table that links a type of plant to a garden.
        Many gardens can have many plants through gardenplants.  Gardenplants
        also contain information specific to when that plant was last watered
        and planted in any specific garden.
    """

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
        """
        Get a gardenplant by its ID.

        :param id: Integer, the ID of the gardenplant (joins table entry).
        :return: A gardenplant object with the provided ID.
        """
        gardenplant = GardenPlant.query.get_or_404(id)
        return gardenplant

    def format_time(date):
        """
        Format the date object into a standard format.

        :param date: A date generated from the datetime module
        :return: String, a string formatted, standardized date.
        """
        return date.strftime("%a, %B %d, %Y")


class Garden(db.Model):
    """
    Garden model from postgresql db.

    The scope of this project only includes a single user with a single garden
        so the current garden is the only garden.  However, if users are
        introduced, one user would have one garden and after setting up the
        reltationship very little would need to change.
    """

    __tablename__ = 'gardens'
    id = db.Column(db.Integer, primary_key=True)

    plants = relationship("Plant", secondary="garden_plants")
    gardenplants = relationship("GardenPlant")

    def current_garden():
        """
        Return the current user's garden.

        See note above, but this is a hard-coded garden since we are not
            implementing users in this version of the application.  This should
            be able to return the Garden object belonging to a logged in user.
        """
        return Garden.query.all()[0]
