# This is app.py to do Step 2 - Climate App of Advanced Data Storage and Retrieval HW

# going to pull in libraries and code that was done previously in climate_starter.ipynb
import numpy as np
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# In the line below, I added connect_args={'check_same_thread': False} to resolve issue stating "SQLite objects created in a thread can only be used in that same thread"
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

# Note: 1 year ago from today was 9-20-2017 and there is no data in Measurement table from that date until now
# so I will try to query 1 year worth of data from the last date in the Measurement table
# This will store latest_date in Measurement table
latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
# Next need to unpack to then store as a string called lat_dat
lat_dat = latest_date[0]
split_lat_dat = lat_dat.split("-")
year_val = int(split_lat_dat[0])
month_val = int(split_lat_dat[1])
day_val = int(split_lat_dat[2])
# determine date 1 year ago from latest date shown in the Measurement table
previous_year_date = dt.date(year_val, month_val, day_val) - dt.timedelta(days=365)

# Want to create a dictionary of precipitation amounts by date where Measurement.date is the key and func.sum(Measurement.prcp) is the value pair
# Query for the dates and precipitation amounts from the last year (1 year worth of data from the last date in the Measurement table)
# also to summarize by date, we will sum the precipitation for each station and use that as the value pair in the dictionary
# so that we report the total preciptation amount across all stations for that particular date
sel_prcp = [Measurement.date, func.sum(Measurement.prcp)]

last_year_prcp_by_date_results = session.query(*sel_prcp).\
    filter(Measurement.date > previous_year_date).\
    group_by(Measurement.date).all()

# Create a stations dictionary from that list of tuples we just found
last_year_prcp_by_date_dict = dict(last_year_prcp_by_date_results)
# Will use last_year_prcp_by_date_dict in the route called /api/v1.0/precipitation below


# Next want to create a dictionary of stations from the dataset where Station.station is the key and Station.name is the value pair
#
# Query columns station and name in Station table. This will output a list of tuples as station_results
station_results = session.query(Station.station, Station.name).all()
# Create a stations dictionary from that list of tuples we just found
stations_dict = dict(station_results)
# Will use stations_dict in the route called /api/v1.0/stations below


# Then want to create a dictionary of temperature observations (tobs) from the most active station where Measurement.date is the key and Measurement.tobs is the value
# Also the date and tobs values are assuming we're only looking at the most active station as determined earlier in the homework
# Also we are only looking at date from the last year (1 year from the last date in the Measurement table)
# Most active station as determined in step 1 of homework assignment was USC00519281
#
# Query columns date and tobs in Measurement table. This will output a list of tuples as most_active_station_date_tobs_results
most_active_station_date_tobs_results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > previous_year_date).\
    filter(Measurement.station == "USC00519281").all()
# Create a most active station tobs dictionary from that list of tuples we just found
most_active_station_tobs_dict = dict(most_active_station_date_tobs_results)
# Will use stations_dict in the route called /api/v1.0/tobs below


from flask import Flask, jsonify

##################################################
# Flask Setup
##################################################
app = Flask(__name__)


##################################################
# Flask Routes
##################################################
# Below is main page
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App API!<br/>"
    )

@app.route("/api/v1.0/precipitation")
def preciptation():
    """Return the last_year_prcp_by_date_dict as json"""
    return jsonify(last_year_prcp_by_date_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return the stations_dict as json"""
    return jsonify(stations_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the most_active_station_tobs_dict as json"""
    return jsonify(most_active_station_tobs_dict)

@app.route("/api/v1.0/<start>")
def calc_temps_by_start(start):
    #This query should return a list of a tuple with first value as TMIN, second value as TAVG, and third value as TMAX
    temps_by_start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    # tmin will be first element inside of the tuple so index[0] will get tuple and another index[0] will get tmin value
    # tavg will be first element inside of the tuple so index[0] will get tuple and another index[1] will get tavg value
    # tmax will be first element inside of the tuple so index[0] will get tuple and another index[2] will get tmax value
    tmin = temps_by_start_results[0][0]
    tavg = temps_by_start_results[0][1]
    tmax = temps_by_start_results[0][2]
    # Create a dictionary where keys will be string names TMIN, TAVG, and TMAX and value pairs will be tmin, tavg, and tmax
    temps_by_start_dict = {'TMIN': tmin, 'TAVG': tavg, 'TMAX': tmax}
    return jsonify(temps_by_start_dict)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps_by_start_end(start, end):
    #This query should return a list of a tuple with first value as TMIN, second value as TAVG, and third value as TMAX
    temps_by_start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # tmin will be first element inside of the tuple so index[0] will get tuple and another index[0] will get tmin value
    # tavg will be first element inside of the tuple so index[0] will get tuple and another index[1] will get tavg value
    # tmax will be first element inside of the tuple so index[0] will get tuple and another index[2] will get tmax value
    tmin = temps_by_start_end_results[0][0]
    tavg = temps_by_start_end_results[0][1]
    tmax = temps_by_start_end_results[0][2]
    # Create a dictionary where keys will be string names TMIN, TAVG, and TMAX and value pairs will be tmin, tavg, and tmax
    temps_by_start_end_dict = {'TMIN': tmin, 'TAVG': tavg, 'TMAX': tmax}
    return jsonify(temps_by_start_end_dict)


if __name__ == "__main__":
    app.run(debug=True)
