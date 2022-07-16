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


# sqla database objects
class Winery(SAFRSBase, db.Model):
    __tablename__ = "winery"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="")
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))
    province_id = db.Column(db.Integer, db.ForeignKey("province.id"))
    country = db.relationship("Country", back_populates="winery")
    province = db.relationship("Province", back_populates="winery")


class Province(SAFRSBase, db.Model):
    __tablename__ = "province"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="")
    winery = db.relationship("Winery", back_populates="province")
    country = db.relationship("Country", back_populates="province")
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))


class Country(SAFRSBase, db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="")
    winery = db.relationship("Winery", back_populates="country")
    province = db.relationship("Province", back_populates="country")


# create the api endpoints
def create_api(app, base_url="localhost", host="localhost", port=4000, api_prefix=""):
    # api = SAFRSAPI(app, host=host, port=port, prefix=api_prefix)
    api = SAFRSAPI(app, host=host, port=port, prefix=api_prefix, title='Wine Data - Country/Winery API',
                   description='A simple Wine data API (wineries and countries)')

    api.expose_object(Country)
    api.expose_object(Winery)
    api.expose_object(Province)
    print(f"Created API: http://{host}:{port}/{api_prefix}")


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
        #os.remove(database_path)
        db.create_all()
        # Populate the db with countries and a wineries and add the winery to the country.winery relationship
        path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(path, '..', 'data', 'wines.csv')
        # makes data frame to hold the world wineries data
        df = pd.read_csv(data_path)
        # Gets a list of unique countries from the data frame
        countries = df.country.unique()

        for country_name in countries:
            # this creates a country model based on Sqlalchemy model
            country = Country()
            country.name = country_name
            # get a list of wineries from the data frame that are in the country selected
            winery = df.loc[df.country == country_name]
            province = df.loc[df.country == country_name]

            # looping through all winery
            for winery_string in winery['winery']:
                # Create a new winery
                winery = Winery()
                # Set the name
                winery.name = winery_string
                # append the city to the country
                country.winery.append(winery)

            # looping through all province
            #for province_string in province['province']:
            #    # Create a new province
            #    province = Province()
            #    # Set the name
             #   province.name = province_string
            #    # append the city to the country
            #    country.province.append(province)

        for province_name in province:
            # this creates a country model based on Sqlalchemy model
            province = Province()
            province.name = province_name
            # get a list of wineries from the data frame that are in the country selected
            winery = df.loc[df.province == province_name]

            # looping through all wineries
            for winery_string in winery['winery']:
                # Create a new winery
                winery = Winery()
                # Set the name
                winery.name = winery_string
                # append the city to the country
                province.winery.append(winery)

        create_api(app, host)

    return app


# address where the api will be hosted, change this if you're not running the app on localhost!
host = sys.argv[1] if sys.argv[1:] else "127.0.0.1"
app = create_app(host=host)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
