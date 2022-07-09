#!/usr/bin/env python3
"""
  This demo application demonstrates the functionality of the safrs documented REST API
  When safrs is installed, you can run this app:
  $ python3 demo_relationship.py [Listener-IP]
  This will run the example on http://Listener-Ip:5000
  - An sqlite database is created and populated
  - A jsonapi rest API is created
  - Swagger documentation is generated
"""
import os
import sys

import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SAFRSAPI

from app.logging_config import logging_setup

db = SQLAlchemy()


# Example sqla database objects
class City(SAFRSBase, db.Model):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="")
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))
    country = db.relationship("Country", back_populates="cities")


class Country(SAFRSBase, db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="")
    cities = db.relationship("City", back_populates="country")


# create the api endpoints
def create_api(app, base_url="localhost", host="localhost", port=4000, api_prefix=""):
    # api = SAFRSAPI(app, host=host, port=port, prefix=api_prefix)
    api = SAFRSAPI(app, host=host, port=port, prefix=api_prefix, title='Wine Data - Country/Winery API',
                   description='A simple Geography API')

    api.expose_object(Country)
    api.expose_object(City)
    # print(f"Created API: http://{host}:{port}/{api_prefix}")


def create_app(config_filename=None, host="localhost"):
    logging_setup()  # create and configure the app

    app = Flask("demo_app")
    path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(path, '..', 'instance', 'file.db')
    app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///" + db_path)
    app.config.update(SQLALCHEMY_TRACK_MODIFICATIONS=False)

    db.init_app(app)

    with app.app_context():
        database_path = os.path.join(path, '..', 'instance', 'file.db')
        os.remove(database_path)
        db.create_all()
        # Populate the db with users and a books and add the book to the user.books relationship
        path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(path, '..', 'data', 'worldcities.csv')
        # makes data frame to hold the world cities data
        df = pd.read_csv(data_path)
        # Gets a list of unique countries from the data frame
        countries = df.country.unique()
        for country_name in countries:
            # this creates a country model based on Sqlalchemy model
            country = Country()
            country.name = country_name
            # get a list of cities from the data frame that are in the country selected
            cities = df.loc[df.country == country_name]
            # looping through all the cities
            for city_string in cities['city_ascii']:
                # Create a new city
                city = City()
                # Set the name
                city.name = city_string
                # append the city to the country
                country.cities.append(city)

        create_api(app, host)

    return app


# address where the api will be hosted, change this if you're not running the app on localhost!
host = sys.argv[1] if sys.argv[1:] else "127.0.0.1"
app = create_app(host=host)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
