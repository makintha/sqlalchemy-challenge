from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station 
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    return (
        f"Welcome to the Homepage of API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>" 
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/(start)<br/>"
        f"/api/v1.0/(start)/(end)"

    )

@app.route("/api/v1.0/precipitation/")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list date and precipitation data"""
    # Query all date and precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[f"{date}"] = prcp
        # prcp_dict["Precipitation"] = prcp
        all_precipitation.append(prcp_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# <start>
@app.route("/api/v1.0/<start>")
def tobs_start(start):
    """When given the start only, calculate TMIN, TAVG, and 
    TMAX for all dates greater than and equal to the start date, or a 404 if not."""

    # canonicalized = start.replace(" ", "").lower()
    start = str(start)
    session = Session(engine)

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    start_date_tobs = session.query(*sel).filter(Measurement.date >= start).all()

    session.close()

    all_start = list(np.ravel(start_date_tobs))

    return jsonify(all_start)



# Start End
@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end(start, end):
    """When given the start only, calculate TMIN, TAVG, and 
    TMAX for all dates greater than and equal to the start date, or a 404 if not."""

    # canonicalized = start.replace(" ", "").lower()
    start = str(start)
    end = str(end)
    session = Session(engine)

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    start_end_tobs = session.query(*sel).filter(Measurement.date.between(start,end)).all()

    session.close()

    all_start = list(np.ravel(start_end_tobs))

    return jsonify(all_start)



# tobs
@app.route("/api/v1.0/tobs")
def tobs():
    """Fetch the dates and temperature observations of the most active station for the last year of data."""

    session = Session(engine)


    station_POI = session.query(Measurement.station, func.count(Measurement.date)).\
        group_by(Measurement.station).order_by(func.count(Measurement.date).desc()).first()
    
    # Query list of temperature observations (TOBS) for the most active station

    most_active_station = session.query(Measurement.tobs).filter(Measurement.date > '2016-12-31').\
        filter(Measurement.station == station_POI[0]).all()

    session.close()
    # Create a dictionary from the row data and append to a list of all_precipitation
    all_tobs = list(np.ravel(most_active_station))

    return jsonify(all_tobs)




if __name__ == "__main__":
    app.run(debug=True)
