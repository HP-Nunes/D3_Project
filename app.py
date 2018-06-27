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

engine = create_engine("sqlite:///db/crimedata2017.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Crime = Base.classes.crimedata2017

#################################################
# Database Setup
#################################################

#db = SQLAlchemy(app)
session = Session(engine)



# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/crimedata2017")
def crimedata2017():
   
    all_crimes = []
    #Grab all the columns we need and create a list
    sel = [Crime.IncidntNum,
        Crime.Category,
        Crime.Descript,
        Crime.DayOfWeek,
        Crime.Date,
        Crime.Time,
        Crime.PdDistrict,
        Crime.Resolution,
        Crime.Address,
        Crime.X,
        Crime.Y]

    results = session.query(*sel).all()
    print(len(results))
    
    df = pd.DataFrame(results, columns=['IncidntNum','Category','Descript',
                                        'DayOfWeek', 'Date', 'Time', 'PdDistrict',
                                        'Resolution', 'Address', 'X', 'Y'])


    # #Create a dictionary to store the values pulled
    # crimes_dict = {}
    #Create an empty list to store a dictionary

    # counter = 0

    # for result in results:

    #     all_crimes.append({
    #         "Incident_Number": result[0],
    #         "Category":result[1],
    #         "Description": result[2],
    #         "DayOfWeek": result[3],
    #         "Date": result[4],
    #         "Time": result[5],
    #         "PdDistrict": result[6],
    #         "Resolution": result[7],
    #         "Address": result[8],
    #         "Lat": result[9],            
    #         "Long": result[10],            
    #     })
    #print(results)
    return jsonify(df.to_dict(orient="records"))
    #     crimes_dict["Incident_Number"] = results[0][1]
    #     crimes_dict["Description"] = results[0][2]
    #     crimes_dict["DayOfWeek"] = results[0][2]
    #     crimes_dict["Date"] = results[0][3]
    #     crimes_dict["Time"] = results[0][4]
    #     crimes_dict["PdDistrict"] = results[0][5]
    #     crimes_dict["Resolution"] = results[0][6]
    #     crimes_dict["Address"] = results[0][7]
    #     crimes_dict["Lat"] = results[0][8]
    #     crimes_dict["Long"] = results[0][9]
    # all_crimes.append(crimes_dict)

   

    #return jsonify(pet_data)

if __name__ == "__main__":
    app.run(debug=True)


#1. Read in CSV into python
#2. Create a sqllite database out of it
#3. Import this database into python and create an engine with automap
#4. Configure the endpoint to return a json