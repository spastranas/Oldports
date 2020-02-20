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
import boto3
import psycopg2 
from botocore.client import Config
from config import S3_KEY, S3_SECRET, S3_BUCKET, API_KEY,DATABASE_URL
app = Flask(__name__, static_url_path='/static')




# the keys are saved under an enviromental variable in both heroku and my local computer.
# https://devcenter.heroku.com/articles/config-vars

# app.config["SECRET_KEY"]= os.environ['AWS_SECRET_ACCESS_KEY']
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/Oldports.sqlite"

# Get config values 
app.config.from_object("config")


# look at configfile
print(app.config)

# define directory for intermediate file upload
UploadDir="static/Images/uploads/"


#################################################
# Database Setup

# postgre

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)






db = SQLAlchemy(app)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)


conn = db.engine.connect()
PictureData = pd.read_sql('SELECT * from "GeoTagData"', conn) #import pandas

app = Flask(__name__, static_url_path='/static')

# route 1

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html", key= API_KEY)
  
# data route
@app.route("/Geodata")
def data():
    # to refresh the database every time we go to the index page

    #################################################
    # Database Setup
    #################################################


    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
    db = SQLAlchemy(app)

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(db.engine, reflect=True)


    conn = db.engine.connect()
    PictureData = pd.read_sql('SELECT * from "GeoTagData"', conn) #import pandas

 
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


    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
    db = SQLAlchemy(app)

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(db.engine, reflect=True)


    conn = db.engine.connect()
    PictureData = pd.read_sql('SELECT * from "GeoTagData"', conn) #import pandas

 
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
            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            
            

            # use function to get geotag data for the picture

            Picname=image.filename
            picAddress=UploadDir +image.filename
            print (picAddress)
            # execute function saved into the updateDatabase.py file(whuch was added at the begining of this app)
            updateDatabase.UpdateDB(picAddress,Picname,DATABASE_URL)
           

            print(image.filename)
            #the above steps will save the pictures into an ephemeral file system, so we have to send it to amazon web services for a permanent location

            

            ACCESS_KEY_ID = S3_KEY
            ACCESS_SECRET_KEY = S3_SECRET
            BUCKET_NAME = S3_BUCKET

            data = open(picAddress, 'rb')

            s3 = boto3.resource(
                's3',
                aws_access_key_id=ACCESS_KEY_ID,
                aws_secret_access_key=ACCESS_SECRET_KEY,
                config=Config(signature_version='s3v4')
            )
            s3.Bucket(BUCKET_NAME).put_object(Key=Picname, Body=data,ACL='public-read')

           






            return redirect(request.url)
    return render_template("public/upload_image.html")






@app.route("/carrusel")
def carrusel():

# to refresh the database every time we go to the index page

    #################################################
    # Database Setup
    #################################################


    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
    db = SQLAlchemy(app)

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(db.engine, reflect=True)


    conn = db.engine.connect()
    PictureData = pd.read_sql('SELECT * from "GeoTagData"', conn) #import pandas

 
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
      



  
if __name__ == "__main__":
    app.run()




