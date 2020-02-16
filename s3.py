import os
 
import pandas as pd
import numpy as np
import ProcessPicture,updateDatabase # this are the functions that will get geodata from pictures and add it to the database

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template,make_response,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask import request, redirect
import sqlite3
from boto.s3.connection import S3Connection
#from helpers import *
app = Flask(__name__, static_url_path='/static')


# the keys are saved under an enviromental variable in both heroku and my local computer.
# connect to WAS s3
s3 = S3Connection(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])
# https://devcenter.heroku.com/articles/config-vars

# app.config["SECRET_KEY"]= os.environ['AWS_SECRET_ACCESS_KEY']
# look at configfile
# print(app.config)



# define directory for file upload

UploadDir="static/Images/uploads/"

#################################################
# Database Setup
#################################################

app.config.from_object("config")



# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/Oldports.sqlite"

# look at configfile
print(app.config)

db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)


conn = db.engine.connect()
PictureData = pd.read_sql("SELECT * from GeoTagData", conn) #import pandas

app = Flask(__name__, static_url_path='/static')

# route 1

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")
  
# data route
@app.route("/Geodata")
def data():
    # to refresh the database every time we go to the index page

    #################################################
    # Database Setup
    #################################################


    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/Oldports.sqlite"
    db = SQLAlchemy(app)

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(db.engine, reflect=True)


    conn = db.engine.connect()
    PictureData = pd.read_sql("SELECT * from GeoTagData", conn) #import pandas

 
# end of refresh get data into a variable that can be jsonified

    df=PictureData
    i = 0
    data=[]

    while i < len(df):
        geodatavar = {

                'FileAddress':list(df['FileAddress'])[i],
                'ImageTimeStamp':list(df['ImageTimeStamp'])[i],
                'city':list(df['city'])[i],
                'country':list(df['country'])[i],
                'landmark':list(df['landmark'])[i],
                'latitude':list(df['latitude'])[i],
                'longitude':list(df['longitude'])[i],
                'state':list(df['state'])[i],
                'zipcode':list(df['zipcode'])[i],
                'index':list(df['index'])[i]
           }
        data.append(geodatavar)
        i+=1
    return jsonify(data)

# individual picture route
@app.route("/latestUpload")
def imageFunct():

# to refresh the database every time we go to the index page

    #################################################
    # Database Setup
    #################################################


    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/Oldports.sqlite"
    db = SQLAlchemy(app)

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(db.engine, reflect=True)


    conn = db.engine.connect()
    PictureData = pd.read_sql("SELECT * from GeoTagData", conn) #import pandas

 
# end of refresh get data into a variable that can be jsonified


    MaxIndex=PictureData["index"].max()
    data=[]
    df=PictureData.loc[(PictureData["index"] == MaxIndex) ]

    i = 0
    data=[]

    while i < len(df):
        geodatavar = {

            'FileAddress':list(df['FileAddress'])[i],
            'ImageTimeStamp':list(df['ImageTimeStamp'])[i],
            'city':list(df['city'])[i],
            'country':list(df['country'])[i],
            'landmark':list(df['landmark'])[i],
            'latitude':list(df['latitude'])[i],
            'longitude':list(df['longitude'])[i],
            'state':list(df['state'])[i],
            'zipcode':list(df['zipcode'])[i],
            'index':list(df['index'])[i]
                          }
        data.append(geodatavar)
        i+=1
    return jsonify(data)
      



# image upload route
@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    # upload picture procedure: https://pythonise.com/feed/flask/flask-uploading-files
    app.config["IMAGE_UPLOADS"] = UploadDir
    
   
    if request.method == "POST":
        if request.files:
            # image = request.files["image"]
            # image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            file = request.files["user_file"]
    # file.filename = secure_filename(file.filename)
            output  = upload_file_to_s3(file, app.config["S3_BUCKET"])
            return str(output)

            # return redirect(request.url)
    return render_template("public/upload_image.html")






@app.route("/carrusel")
def carrusel():

# to refresh the database every time we go to the index page

    #################################################
    # Database Setup
    #################################################


    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/Oldports.sqlite"
    db = SQLAlchemy(app)

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(db.engine, reflect=True)


    conn = db.engine.connect()
    PictureData = pd.read_sql("SELECT * from GeoTagData", conn) #import pandas

 
# end of refresh get data into a variable that can be jsonified


    MaxIndex=PictureData["index"].max()
    data=[]
    df=PictureData.loc[(PictureData["index"] > MaxIndex-3) ]

    i = 0
    data=[]

    while i < len(df):
        geodatavar = {

            'FileAddress':list(df['FileAddress'])[i],
            'ImageTimeStamp':list(df['ImageTimeStamp'])[i],
            'city':list(df['city'])[i],
            'country':list(df['country'])[i],
            'landmark':list(df['landmark'])[i],
            'latitude':list(df['latitude'])[i],
            'longitude':list(df['longitude'])[i],
            'state':list(df['state'])[i],
            'zipcode':list(df['zipcode'])[i],
            'index':list(df['index'])[i]
                          }
        data.append(geodatavar)
        i+=1
    return jsonify(data)
      




# @app.route("/upload-image", methods=["GET", "POST"])

@app.route("/test", methods=["POST"])
def upload_file():

    file = request.files["user_file"]
    # file.filename = secure_filename(file.filename)
    output  = upload_file_to_s3(file, app.config["S3_BUCKET"])
    return str(output)




    
if __name__ == "__main__":
    app.run()




