import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():

    return(
        f"Welcome to Hawaii Climate Analysis<br/> "
        f"Available Routes:<br/>"
        f"<br/>"  
        f"Precipitation data with dates:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Stations and names:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temprture observations:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Min, Max. and Avg. temperatures for given start date: (use date format:'yyyy-mm-dd'):<br/>"
        f"/api/v1.0/&lt;start&gt;<br>"
        f"<br/>"
        f"Min. Max. and Avg. tempratures for given start and end date: (use date format: 'yyyy-mm-dd'/'yyyy-mm-dd' for start date and end date values):<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
        f"<br/>"
        f"i.e. <a href='/api/v1.0/min_max_avg/2012-01-01/2016-12-31' target='_blank'>/api/v1.0/min_max_avg/2012-01-01/2016-12-31</a>"
)

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    precipitation = []
    for result in results:
            r = {}
            r[result[0]] = result[1]
            precipitation.append(r)

    return jsonify(precipitation) 

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name).all()
    session.close()
    
    station_list = []
    for result in results:
        r = {}
        r["station"]= result[0]
        r["name"] = result[1]
        station_list.append(r)
    return jsonify(station_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start, end = None):
    session = Session(engine)
    if not end:
        results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    else:
        results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date < end).all()
    final_results = list(np.ravel(results))
    return jsonify(temps = final_results)
    session.close()

if __name__ == "__main__":
    app.run(debug=True)