###########################
# Dependencies
###########################
#Set up Flask (Server)
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#SQL Alchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc, select
from flask_sqlalchemy import SQLAlchemy


import pandas as pd
import numpy as np
import os

###########################
# Flask Setup
###########################
#create the engine with sqlite
app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db/crimedata2017.sqlite"

engine = create_engine("sqlite:///db/crimedata.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

Crime2017 = Base.classes.crimedata2017
Crime2018 = Base.classes.crimedata2018

#################################################
# Database Setup
#################################################

#db = SQLAlchemy(app)
session = Session(engine)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/crimedata")
def crimedata():
   
    #Grab all the columns we need and create a list
    sel2017 = [Crime2017.IncidntNum,
        Crime2017.Category,
        Crime2017.Descript,
        Crime2017.DayOfWeek,
        Crime2017.Date,
        Crime2017.Time,
        Crime2017.PdDistrict,
        Crime2017.Resolution,
        Crime2017.Address,
        Crime2017.X,
        Crime2017.Y]

    sel2018 = [Crime2018.IncidntNum,
        Crime2018.Category,
        Crime2018.Descript,
        Crime2018.DayOfWeek,
        Crime2018.Date,
        Crime2018.Time,
        Crime2018.PdDistrict,
        Crime2018.Resolution,
        Crime2018.Address,
        Crime2018.X,
        Crime2018.Y]    

    results2017 = session.query(*sel2017)
    results2018 = session.query(*sel2018)

    #Perform a Union All to combine the 2 datasets
    results = results2017.union_all(results2018).all()
    print(len(results))

    #Store results into a dataframe
    df = pd.DataFrame(results, columns=['IncidntNum','Category','Descript',
                                        'DayOfWeek', 'Date', 'Time', 'PdDistrict',
                                        'Resolution', 'Address', 'X', 'Y'])

    #Return the dataframe in json format
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)


#1. Read in CSV into python
#2. Create a sqllite database out of it
#3. Import this database into python and create an engine with automap
#4. Configure the endpoint to return a json